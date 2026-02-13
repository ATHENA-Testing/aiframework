import os
import re
import ast
import glob
import yaml
import json
import sys
from ai.ai_executor import AIExecutor
from ai.prompt_library import PromptLibrary
from ai.rag_engine import RAGEngine
from utils.global_scanner import GlobalScanner

class AICodeGenerator:
    def __init__(self):
        try:
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

            for line in lines:
                line = line.strip()
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

    def generate_feature_from_requirement(self, requirement_path):
        try:
            if not self.executor.enabled:
                return None
            with open(requirement_path, 'r', encoding='utf-8') as f:
                req_text = f.read()
            
            # Improved Multi-line Parsing for user_story.txt
            # Ensure the text is cleaned but maintains its structure for the LLM
            req_text = req_text.strip()
            
            # Check for JIRA ID
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
            
            # Error Check: If LLM returned an error message instead of Gherkin
            if feature_content.startswith("Error from LLM Provider") or feature_content.startswith("Failed to generate"):
                print(f"AI Generation Error: {feature_content}")
                return None
                
            feature_content = re.sub(r'```gherkin|```', '', feature_content).strip()
            
            # Sanity check for Gherkin content
            if "Feature:" not in feature_content:
                print(f"Warning: Generated content for {requirement_path} does not look like Gherkin.")
                
            base_name = os.path.basename(requirement_path).replace('.txt', '.feature')
            feature_path = f"features/{base_name}"
            with open(feature_path, 'w', encoding='utf-8') as f:
                f.write(feature_content)
            return feature_path, feature_content
        except Exception as e:
            print(f"Error in generate_feature_from_requirement for {requirement_path}: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def process_all(self):
        try:
            self.rag.rebuild_index()
            response_content = "### AI GENERATION RESPONSE SUMMARY ###\n\n"
            
            req_pattern = os.path.join("requirements", "*.txt")
            req_files = glob.glob(req_pattern)
            
            if not req_files:
                print("No requirement files found in requirements/ folder.")
                return

            for req in req_files:
                if "Response.txt" in req: continue
                
                print(f"Processing requirement: {req}")
                result = self.generate_feature_from_requirement(req)
                if not result: 
                    print(f"Skipping {req} due to generation failure.")
                    continue
                    
                f_path, f_content = result
                
                response_content += f"--- FEATURE: {os.path.basename(f_path)} ---\n{f_content}\n\n"
                summary = self.sync_feature_to_code(f_path)
                
                response_content += "--- STEP DEFINITIONS ---\n"
                if summary["steps"]:
                    response_content += "\n".join(summary["steps"]) + "\n\n"
                else:
                    response_content += "No new steps generated (all reused or failed).\n\n"
                    
                response_content += "--- PAGE METHODS ---\n"
                if summary["methods"]:
                    response_content += "\n".join(summary["methods"]) + "\n\n"
                else:
                    response_content += "No new methods generated (all reused or failed).\n\n"
                
            self.process_smart_prompts()
            
            with open("requirements/Response.txt", 'w', encoding='utf-8') as f:
                f.write(response_content)
            print("Response.txt generated in requirements/ folder.")

            # Git Push if enabled
            if self.git:
                print("Git integration enabled. Pushing changes...")
                self.git.commit_and_push("AI Generated automation code and features")
                
        except Exception as e:
            print(f"Error during process_all: {e}")
            import traceback
            traceback.print_exc()

    def process_smart_prompts(self, directory="pages"):
        try:
            pattern = os.path.join(directory, "**", "*.py")
            for file in glob.glob(pattern, recursive=True):
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                prompts = re.findall(r'# AI: (.*)', content)
                if not prompts: continue
                
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
