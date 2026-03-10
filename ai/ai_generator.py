import os
import re
import ast
import glob
import yaml
import json
import sys
import traceback
import requests  # for preflight probe

from ai.ai_executor import AIExecutor
from ai.prompt_library import PromptLibrary
from ai.rag_engine import RAGEngine
from utils.global_scanner import GlobalScanner


# ------------------------------
# Environment defaults (proxy bypass + host)
# ------------------------------
# Ensure local loopback is never routed through a proxy
os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1")
# Prefer 127.0.0.1 over localhost to avoid proxy/VPN quirks
os.environ.setdefault("OLLAMA_HOST", "http://127.0.0.1:11434")

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")


def preflight_probe(host: str = OLLAMA_HOST, timeout: int = 10) -> None:
    """
    Fast connectivity/health check against Ollama: GET /api/tags.
    Raises a RuntimeError with precise details if unreachable.
    """
    url = f"{host}/api/tags"
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
    except Exception as e:
        raise RuntimeError(f"Preflight probe failed for {url}: {e!r}")


def looks_like_gherkin(text: str) -> bool:
    """
    Minimal Gherkin sanity: require both 'Feature:' and 'Scenario:'.
    """
    return ("Feature:" in text) and ("Scenario:" in text)


def looks_like_llm_error(text: str) -> bool:
    """
    Heuristic to catch provider error strings that arrive as plain text.
    Extend this list as needed.
    """
    patterns = [
        r"endpoint not found",
        r"Read timed out",
        r"Failed to generate",
        r"Error from LLM Provider",
        r"HTTPConnectionPool",
        r"ConnectionError",
        r"timed out",
        r"Bad gateway",
        r"502",
        r"503",
        r"504",
    ]
    low = text.strip().lower()
    return any(pat.lower() in low for pat in patterns)


class AICodeGenerator:
    def __init__(self):
        try:
            # Early probe — fail fast with accurate error if Ollama is not reachable
            preflight_probe(OLLAMA_HOST, timeout=10)

            self.executor = AIExecutor()
            self.prompt_lib = PromptLibrary()
            self.rag = RAGEngine()
            self.scanner = GlobalScanner()

            config_path = "config/framework.yaml"
            if not os.path.exists(config_path):
                print(f"Error: {config_path} not found.")
                sys.exit(1)

            with open(config_path, 'r') as f:
                self.framework_config = yaml.safe_load(f)

            # Conditional JIRA Connector
            self.jira = None
            if self.framework_config.get('jira', {}).get('enabled', False):
                try:
                    from connectors.jira_connector import JiraConnector
                    self.jira = JiraConnector()
                except Exception as e:
                    print(f"Warning: Failed to initialize JIRA connector: {e}")

            # Conditional Git Connector
            self.git = None
            if self.framework_config.get('git', {}).get('enabled', False):
                try:
                    from connectors.git_connector import GitConnector
                    self.git = GitConnector()
                except Exception as e:
                    print(f"Warning: Failed to initialize Git connector: {e}")

            ai_config_path = "config/ai.yaml"
            if not os.path.exists(ai_config_path):
                print(f"Error: {ai_config_path} not found.")
                sys.exit(1)

            with open(ai_config_path, 'r') as f:
                self.ai_config = yaml.safe_load(f)['ai']

        except Exception as e:
            print(f"Critical Error in AICodeGenerator init: {e}")
            sys.exit(1)

    def append_to_file(self, file_path, code):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("from behave import given, when, then\n" if "steps" in file_path else "")

            with open(file_path, 'a', encoding='utf-8') as f:
                f.write("\n" + code + "\n")
        except Exception as e:
            print(f"Error appending to {file_path}: {e}")

    def sync_feature_to_code(self, feature_path):
        try:
            print(f"Syncing feature: {feature_path}")
            with open(feature_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            feature_name = os.path.basename(feature_path).replace('.feature', '')
            target_page = f"pages/{feature_name}_page.py"
            target_steps = f"features/steps/{feature_name}_steps.py"

            step_map = self.scanner.get_all_step_definitions()
            existing_methods = self.scanner.get_all_page_methods()
            generated_summary = {"steps": [], "methods": []}

            for raw in lines:
                line = raw.strip()
                if any(line.startswith(kw) for kw in ['Given', 'When', 'Then', 'And', 'But']):
                    step_text = re.sub(r'^(Given|When|Then|And|But)\s+', '', line)

                    if step_text not in step_map:
                        print(f"Detected new/updated step: {step_text}")
                        rag_context = self.rag.query(step_text)

                        # 1. Generate Page Method
                        page_prompt = self.prompt_lib.PAGE_METHOD_GENERATION_PROMPT.format(
                            rag_context=rag_context,
                            existing_methods=", ".join(existing_methods.keys()),
                            action_description=f"Perform action for: {step_text}. ENSURE 100% AC COVERAGE."
                        )
                        page_code = self.executor.provider.generate(page_prompt).strip()
                        page_code = re.sub(r'```python|```', '', page_code).strip()

                        if "# Use existing method" not in page_code and page_code:
                            self.append_to_file(target_page, page_code)
                            generated_summary["methods"].append(page_code)
                        elif "# Use existing method" in page_code:
                            generated_summary["methods"].append(page_code)

                        # 2. Generate Step Definition
                        step_prompt = self.prompt_lib.STEP_DEFINITION_GENERATION_PROMPT.format(
                            step_text=line,
                            existing_steps=", ".join(step_map.keys()),
                            page_methods=", ".join(self.scanner.get_all_page_methods().keys())
                        )
                        step_code = self.executor.provider.generate(step_prompt).strip()
                        step_code = re.sub(r'```python|```', '', step_code).strip()

                        if "# Step already exists" not in step_code and step_code:
                            self.append_to_file(target_steps, step_code)
                            generated_summary["steps"].append(step_code)
                        elif "# Step already exists" in step_code:
                            generated_summary["steps"].append(f"# Reused existing step for: {line}")

            return generated_summary
        except Exception as e:
            print(f"Error in sync_feature_to_code: {e}")
            return {"steps": [], "methods": []}

    def _repair_to_gherkin(self, text: str, model_name: str) -> str:
        """
        Attempt a one-shot repair if the first generation wasn't strict Gherkin.
        """
        repair_prompt = (
            "Rewrite the following strictly as valid Gherkin with:\n"
            "Feature: <title>\n"
            "Scenario: <title>\n"
            "Given ...\nWhen ...\nThen ...\n\n"
            "Return ONLY Gherkin—no commentary or code fences.\n\n"
            f"{text}"
        )
        repaired = self.executor.provider.generate(repair_prompt).strip()
        repaired = re.sub(r'```gherkin|```', '', repaired).strip()
        return repaired

    def generate_feature_from_requirement(self, requirement_path):
        """
        Returns (feature_path, feature_content) on success, or raises RuntimeError with a precise message.
        """
        try:
            if not self.executor.enabled:
                raise RuntimeError("AI executor/provider is disabled in configuration.")

            with open(requirement_path, 'r', encoding='utf-8') as f:
                req_text = f.read().strip()

            # Optional JIRA enrichment
            jira_match = re.search(r'JIRA:\s*([A-Z]+-\d+)', req_text)
            if jira_match and self.jira:
                issue_key = jira_match.group(1)
                print(f"Fetching JIRA details for {issue_key}...")
                jira_data = self.jira.get_issue_details(issue_key)
                if jira_data:
                    jira_prompt = self.prompt_lib.JIRA_REQUIREMENT_PROMPT.format(
                        jira_data=json.dumps(jira_data, indent=2)
                    )
                    req_text = self.executor.provider.generate(jira_prompt).strip()
                    print(f"JIRA requirement processed for {issue_key}")
            elif jira_match and not self.jira:
                print(f"Warning: JIRA ID {jira_match.group(1)} found but JIRA integration is disabled in framework.yaml.")

            rag_context = self.rag.query(req_text)
            existing_steps = self.scanner.get_all_feature_steps()

            prompt = self.prompt_lib.FEATURE_GENERATION_PROMPT.format(
                rag_context=rag_context,
                requirement_text=req_text,
                existing_steps=", ".join(existing_steps)
            )

            feature_content = self.executor.provider.generate(prompt).strip()

            # Normalize & strip code fences
            feature_content = re.sub(r'```gherkin|```', '', feature_content).strip()

            # Reject obvious provider error payloads
            if looks_like_llm_error(feature_content):
                raise RuntimeError(f"Provider returned error-like text: {feature_content[:160]}...")

            # Gherkin sanity; attempt a repair if needed
            if not looks_like_gherkin(feature_content):
                print(f"Warning: Generated content for {requirement_path} does not look like Gherkin. Attempting repair...")
                repaired = self._repair_to_gherkin(feature_content, self.ai_config.get("model", ""))
                if looks_like_llm_error(repaired):
                    raise RuntimeError(f"Provider returned error-like text (repair pass): {repaired[:160]}...")
                if not looks_like_gherkin(repaired):
                    raise RuntimeError("Generated content is not valid Gherkin after repair pass.")
                feature_content = repaired

            base_name = os.path.basename(requirement_path).replace('.txt', '.feature')
            feature_path = f"features/{base_name}"
            os.makedirs(os.path.dirname(feature_path), exist_ok=True)
            with open(feature_path, 'w', encoding='utf-8') as f:
                f.write(feature_content)

            return feature_path, feature_content

        except Exception as e:
            # Raise upwards so process_all can write a precise message to Response.txt
            raise RuntimeError(f"{os.path.basename(requirement_path)}: {e}")

    def process_all(self):
        """
        Rebuilds the KB, processes all requirements -> features, syncs steps/pages,
        and writes an accurate Response.txt (no stale localhost text).
        """
        try:
            # Rebuild index first
            self.rag.rebuild_index()

            response_lines = ["### AI GENERATION RESPONSE SUMMARY ###", ""]

            req_files = glob.glob(os.path.join("requirements", "*.txt"))
            if not req_files:
                print("No requirement files found in requirements/ folder.")
                return

            for req in req_files:
                if req.endswith("Response.txt"):
                    continue

                base_name = os.path.basename(req)
                print(f"Processing requirement: {req}")

                try:
                    f_path, f_content = self.generate_feature_from_requirement(req)

                    # Append generated feature content
                    response_lines.append(f"--- FEATURE: {os.path.basename(f_path)} ---")
                    response_lines.append(f_content)
                    response_lines.append("")

                    # Sync to code (steps/pages)
                    summary = self.sync_feature_to_code(f_path)

                    response_lines.append("--- STEP DEFINITIONS ---")
                    if summary["steps"]:
                        response_lines.extend(summary["steps"])
                        response_lines.append("")
                    else:
                        response_lines.append("No new steps generated (all reused or failed).")
                        response_lines.append("")

                    response_lines.append("--- PAGE METHODS ---")
                    if summary["methods"]:
                        response_lines.extend(summary["methods"])
                        response_lines.append("")
                    else:
                        response_lines.append("No new methods generated (all reused or failed).")
                        response_lines.append("")

                except Exception as e:
                    # Accurate message—no hard-coded http://localhost text
                    response_lines.append(f"--- FEATURE: {base_name.replace('.txt', '.feature')} ---")
                    response_lines.append(f"AI Generation Error: {e}")
                    response_lines.append("")
                    print(f"Skipping {req} due to generation failure: {e}")

            # Process in-file smart prompts after features/steps/pages
            self.process_smart_prompts()

            # Write Response.txt (truncate & write fresh)
            os.makedirs("requirements", exist_ok=True)
            with open("requirements/Response.txt", 'w', encoding='utf-8') as f:
                f.write("\n".join(response_lines))
            print("Response.txt generated in requirements/ folder.")

            # Git Push if enabled
            if self.git:
                print("Git integration enabled. Pushing changes...")
                self.git.commit_and_push("AI Generated automation code and features")

        except Exception as e:
            print(f"Error during process_all: {e}")
            traceback.print_exc()

    def process_smart_prompts(self, directory="pages"):
        try:
            pattern = os.path.join(directory, "**", "*.py")
            for file in glob.glob(pattern, recursive=True):
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()

                prompts = re.findall(r'# AI: (.*)', content)
                if not prompts:
                    continue

                for prompt_text in prompts:
                    rag_context = self.rag.query(prompt_text)
                    existing_methods = self.scanner.get_all_page_methods()
                    ai_prompt = self.prompt_lib.LOGIC_GENERATION_PROMPT.format(
                        user_prompt=prompt_text + f"\nContext from knowledge base: {rag_context}",
                        existing_methods=", ".join(existing_methods.keys())
                    )
                    generated_code = self.executor.provider.generate(ai_prompt).strip()
                    generated_code = re.sub(r'```python|```', '', generated_code).strip()
                    full_prompt_line = f"# AI: {prompt_text}"
                    content = content.replace(full_prompt_line, generated_code)

                with open(file, 'w', encoding='utf-8') as f:
                    f.write(content)
        except Exception as e:
            print(f"Error in process_smart_prompts: {e}")


if __name__ == "__main__":
    generator = AICodeGenerator()
    generator.process_all()
