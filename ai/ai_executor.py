import os
import yaml
from ai.llm_provider import LLMFactory
from ai.prompt_library import PromptLibrary
from ai.ollama_adapter import OllamaProvider  # <-- NEW: our safe Ollama adapter


class AIExecutor:
    """
    Central AI execution/routing.

    - Reads config/ai.yaml -> ai.*
    - If provider == 'ollama', builds an OllamaProvider that:
        * Honors OLLAMA_HOST (defaults to http://127.0.0.1:11434)
        * Bypasses proxies for localhost/127.0.0.1
        * Preflight probes /api/tags (fail-fast with precise error)
        * Uses long timeouts + retries + backoff
      Otherwise, falls back to your existing LLMFactory providers.

    - _get_provider_for_task() preserves your routing (review/assertion/etc).
    """

    def __init__(self, config_path: str = "config/ai.yaml"):
        self.config = self._load_config(config_path)
        self.enabled = self.config.get("enabled", False)
        self.mode = self.config.get("mode", "off")
        self.routing = self.config.get("routing", {}) or {}

        # Default provider for general use
        if self.enabled:
            try:
                self.provider = self._build_provider(self.config)
            except Exception as e:
                # Disable gracefully if provider cannot be built
                self.enabled = False
                self.provider = None
                raise
        else:
            self.provider = None

    # -------------------------
    # Config helpers
    # -------------------------
    def _load_config(self, path: str) -> dict:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return (yaml.safe_load(f) or {}).get("ai", {}) or {}
        return {}

    def _merge_config_for_provider(self, provider_name: str) -> dict:
        """
        Merge top-level ai.* config with ai.<provider_name> overrides (if present),
        and set 'provider' explicitly to provider_name.
        """
        merged = dict(self.config)  # shallow copy
        merged["provider"] = provider_name
        if provider_name in self.config and isinstance(self.config[provider_name], dict):
            merged.update(self.config[provider_name])
        return merged

    def _build_provider(self, cfg: dict):
        """
        Factory that chooses OllamaAdapter for 'ollama' or falls back to your LLMFactory.
        """
        provider = (cfg.get("provider") or "").strip().lower()
        model = cfg.get("model", "llama2:latest")
        timeout_sec = int(cfg.get("timeout_sec", 6000))
        retries = int(cfg.get("retries", 5))
        backoff = float(cfg.get("backoff", 2.0))

        if provider == "ollama":
            # Ensure env has safe defaults for loopback
            os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1")
            os.environ.setdefault("OLLAMA_HOST", os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434"))
            return OllamaProvider(
                model=model,
                timeout_sec=timeout_sec,
                retries=retries,
                backoff=backoff,
            )
        else:
            # Use your existing providers (OpenAI/Gemini/Groq/etc.) via LLMFactory
            return LLMFactory.get_provider(cfg)

    # -------------------------
    # Routing
    # -------------------------
    def _get_provider_for_task(self, task_type: str):
        """
        Returns a provider instance based on routing map, or the default provider.
        Respects per-provider sub-config blocks in ai.yaml.
        """
        if not self.enabled:
            return None

        provider_name = (self.routing.get(task_type) or "").strip().lower()
        if provider_name:
            temp_cfg = self._merge_config_for_provider(provider_name)
            return self._build_provider(temp_cfg)

        return self.provider

    # -------------------------
    # Execution helpers
    # -------------------------
    def execute_review(self, code: str) -> str:
        if not self.enabled or self.mode not in ["review", "generate"]:
            return "AI Review is disabled or mode not set to review."
        provider = self._get_provider_for_task("review") or self.provider
        prompt = PromptLibrary.CODE_REVIEW_PROMPT.format(code=code)
        return provider.generate(prompt)

    def execute_assert(self, condition: str, context_data: str) -> str:
        if not self.enabled:
            return "AI is disabled."
        provider = self._get_provider_for_task("assertion") or self.provider
        prompt = (
            f"Act as a QA Engineer. Verify the following condition: {condition}. "
            f"Context: {context_data}. Return 'PASS' or 'FAIL' with a brief reason."
        )
        return provider.generate(prompt)

    def suggest_method(self, description: str) -> str:
        if not self.enabled or self.mode not in ["assist", "generate"]:
            return "AI Assistance is disabled."
        prompt = PromptLibrary.METHOD_SUGGESTION_PROMPT.format(description=description)
        return self.provider.generate(prompt)

    def generate_steps(self, feature_text: str) -> str:
        if not self.enabled or self.mode != "generate":
            return "AI Generation is disabled."
        prompt = PromptLibrary.STEP_GENERATION_PROMPT.format(feature_text=feature_text)
        return self.provider.generate(prompt)

    def get_quick_fix(self, file_path: str, error_message: str) -> str:
        if not self.enabled:
            return "AI is disabled."
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            return f"Failed to read file for quick fix: {str(e)}"
        prompt = PromptLibrary.QUICK_FIX_PROMPT.format(
            file_path=file_path,
            error_message=error_message,
            file_content=content,
        )
        return self.provider.generate(prompt)