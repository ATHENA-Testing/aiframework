import os
import json
import time
import requests


# -----------------------------
# Shared helpers
# -----------------------------
def _sleep_backoff(attempt: int, base: float = 2.0):
    time.sleep(base ** attempt)


# -----------------------------
# Base interface
# -----------------------------
class LLMProvider:
    def generate(self, prompt: str) -> str:
        raise NotImplementedError


# -----------------------------
# OpenAI Provider
# -----------------------------
class OpenAIProvider(LLMProvider):
    def __init__(self, api_key=None, model="gpt-4o-mini", base_url=None, timeout=6600, retries=3):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.model = model
        self.base_url = (base_url or os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
        self.timeout = int(timeout)
        self.retries = int(retries)

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            return "Failed to generate response from OpenAI: missing API key."

        # Try the requested model first; then a couple of sensible fallbacks
        models_to_try = [self.model, "gpt-4o-mini", "gpt-3.5-turbo"]
        # De-dup while preserving order
        models_to_try = list(dict.fromkeys([m for m in models_to_try if m]))

        last_error = "Unknown error"
        for model in models_to_try:
            for attempt in range(self.retries):
                try:
                    headers = {
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    }
                    payload = {
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7,
                    }
                    resp = requests.post(
                        f"{self.base_url}/chat/completions",
                        headers=headers,
                        json=payload,
                        timeout=self.timeout,
                    )

                    if resp.status_code == 429:
                        last_error = f"OpenAI rate limit for model '{model}'."
                        if attempt < self.retries - 1:
                            _sleep_backoff(attempt)
                            continue
                        break

                    resp.raise_for_status()
                    data = resp.json()
                    if "choices" in data and data["choices"]:
                        return data["choices"][0]["message"]["content"]
                    last_error = f"Unexpected OpenAI response for model '{model}': {json.dumps(data)}"
                    break

                except Exception as e:
                    last_error = f"{type(e).__name__}: {e}"
                    if attempt < self.retries - 1:
                        _sleep_backoff(attempt)
                        continue
                    break

        return f"Failed to generate response from OpenAI after retries. Last error: {last_error}"


# -----------------------------
# Gemini Provider
# -----------------------------
class GeminiProvider(LLMProvider):
    def __init__(self, api_key=None, model="gemini-1.5-flash", timeout=6600, retries=3):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "")
        self.model = model
        self.timeout = int(timeout)
        self.retries = int(retries)
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            return "Failed to generate response from Gemini: missing API key."

        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        last_error = None
        for attempt in range(self.retries):
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
                resp.raise_for_status()
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
                last_error = f"{type(e).__name__}: {e}"
                if attempt < self.retries - 1:
                    _sleep_backoff(attempt)
                    continue
                break

        return f"Failed to generate response from Gemini after retries. Last error: {last_error}"


# -----------------------------
# Groq Provider (OpenAI-compatible API)
# -----------------------------
class GroqProvider(LLMProvider):
    def __init__(self, api_key=None, model="llama3-8b-8192", timeout=6600, retries=3):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY", "")
        self.model = model
        self.timeout = int(timeout)
        self.retries = int(retries)
        self.base_url = "https://api.groq.com/openai/v1"

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            return "Failed to generate response from Groq: missing API key."

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {"model": self.model, "messages": [{"role": "user", "content": prompt}]}

        last_error = None
        for attempt in range(self.retries):
            try:
                resp = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=self.timeout)
                resp.raise_for_status()
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                last_error = f"{type(e).__name__}: {e}"
                if attempt < self.retries - 1:
                    _sleep_backoff(attempt)
                    continue
                break

        return f"Failed to generate response from Groq after retries. Last error: {last_error}"


# -----------------------------
# Ollama Provider (Local)
# -----------------------------
def _ollama_host() -> str:
    """
    Prefer OLLAMA_HOST from env; default to 127.0.0.1 (safer than 'localhost' behind proxies/VPNs).
    """
    return os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")


def _ollama_preflight(host: str, timeout: int = 10):
    """
    Fast health check against Ollama: GET /api/tags. Raises with precise details on failure.
    """
    url = f"{host}/api/tags"
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()


class OllamaProvider(LLMProvider):
    """
    Local Ollama provider (safe defaults):
      - NO_PROXY for loopback
      - OLLAMA_HOST (default http://127.0.0.1:11434)
      - preflight probe
      - long timeout + retries/backoff
      - accurate errors (no hardcoded 'localhost endpoint not found')
    """

    def __init__(self, host=None, model="llama2:latest", timeout=6600, retries=5, backoff=2.0, num_predict=None, temperature=None, top_p=None):
        # Ensure loopback never goes through a proxy
        os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1")

        self.host = (host or _ollama_host()).rstrip("/")
        self.model = model
        self.timeout = int(timeout)
        self.retries = int(retries)
        self.backoff = float(backoff)

        # Optional generation controls
        self.default_options = {}
        if num_predict is not None:
            self.default_options["num_predict"] = int(num_predict)
        if temperature is not None:
            self.default_options["temperature"] = float(temperature)
        if top_p is not None:
            self.default_options["top_p"] = float(top_p)

        # Fail fast if unreachable (precise message)
        _ollama_preflight(self.host, timeout=10)

    def generate(self, prompt: str) -> str:
        url = f"{self.host}/api/generate"
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        if self.default_options:
            payload["options"] = self.default_options

        last_error = None
        for attempt in range(self.retries):
            try:
                resp = requests.post(url, json=payload, timeout=self.timeout)
                resp.raise_for_status()
                data = resp.json()
                return data.get("response", f"Unexpected Ollama response format: {json.dumps(data)}")
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
                last_error = f"{type(e).__name__}: {e}"
                if attempt < self.retries - 1:
                    _sleep_backoff(attempt, self.backoff)
                    continue
                break
            except Exception as e:
                return f"Failed to generate response from Ollama (to {url}): {type(e).__name__}: {e}"

        return f"Failed to generate response from Ollama after retries (to {url}). Last error: {last_error}"


# -----------------------------
# Azure OpenAI Provider
# -----------------------------
class AzureOpenAIProvider(LLMProvider):
    def __init__(self, endpoint=None, api_key=None, deployment_name=None, timeout=6600, retries=3):
        self.endpoint = (endpoint or "").rstrip("/")
        self.api_key = api_key or os.environ.get("AZURE_OPENAI_API_KEY", "")
        self.deployment_name = deployment_name or os.environ.get("AZURE_OPENAI_DEPLOYMENT", "")
        self.timeout = int(timeout)
        self.retries = int(retries)

    def generate(self, prompt: str) -> str:
        if not self.endpoint or not self.api_key or not self.deployment_name:
            return "Failed to generate response from Azure OpenAI: missing endpoint/api_key/deployment."

        headers = {"Content-Type": "application/json", "api-key": self.api_key}
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 2000,
        }
        url = f"{self.endpoint}/openai/deployments/{self.deployment_name}/chat/completions?api-version=2023-05-15"

        last_error = None
        for attempt in range(self.retries):
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
                resp.raise_for_status()
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            except Exception as e:
                last_error = f"{type(e).__name__}: {e}"
                if attempt < self.retries - 1:
                    _sleep_backoff(attempt)
                    continue
                break

        return f"Failed to generate response from Azure OpenAI after retries. Last error: {last_error}"


# -----------------------------
# Factory
# -----------------------------
class LLMFactory:
    @staticmethod
    def get_provider(config: dict) -> LLMProvider:
        """
        Builds a provider from ai.yaml-style config.
        (AIExecutor may override Ollama routing to a dedicated adapter;
         this factory remains safe for other providers and still robust for Ollama.)
        """
        provider_type = (config.get("provider", "openai") or "").lower().strip()
        timeout = int(config.get("timeout_sec", 600))
        retries = int(config.get("retries", 5))
        backoff = float(config.get("backoff", 2.0))

        if provider_type == "openai":
            return OpenAIProvider(
                api_key=config.get("api_key"),
                model=config.get("model", "gpt-4o-mini"),
                base_url=config.get("base_url"),
                timeout=timeout,
                retries=retries,
            )

        if provider_type == "gemini":
            return GeminiProvider(
                api_key=config.get("api_key"),
                model=config.get("model", "gemini-1.5-flash"),
                timeout=timeout,
                retries=retries,
            )

        if provider_type == "groq":
            return GroqProvider(
                api_key=config.get("api_key"),
                model=config.get("model", "llama3-8b-8192"),
                timeout=timeout,
                retries=retries,
            )

        if provider_type == "ollama":
            # Prefer OLLAMA_HOST env; fallback to ai.yaml -> ai.ollama.host; default to 127.0.0.1
            host = os.getenv("OLLAMA_HOST", (config.get("ollama", {}) or {}).get("host", "http://127.0.0.1:11434"))
            return OllamaProvider(
                host=host,
                model=config.get("model", "llama2:latest"),
                timeout=timeout,
                retries=retries,
                backoff=backoff,
                # optional generation controls (if present)
                num_predict=config.get("num_predict"),
                temperature=config.get("temperature"),
                top_p=config.get("top_p"),
            )

        if provider_type == "azure":
            azure_cfg = config.get("azure", {}) or {}
            return AzureOpenAIProvider(
                endpoint=azure_cfg.get("endpoint"),
                api_key=config.get("api_key"),
                deployment_name=azure_cfg.get("deployment_name"),
                timeout=timeout,
                retries=retries,
            )

        raise ValueError(f"Unsupported LLM provider: {provider_type}")