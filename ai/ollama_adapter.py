import os
import time
import requests


def _get_host() -> str:
    # Prefer env; default to 127.0.0.1 (safer than 'localhost' behind proxies/VPNs)
    return os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")


def _preflight_probe(host: str, timeout: int = 10) -> None:
    """
    Fast health check against Ollama: GET /api/tags.
    Raises on failure with precise message (never a generic 'endpoint not found').
    """
    url = f"{host}/api/tags"
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()


class OllamaProvider:
    """
    Minimal Ollama provider with:
      - proxy bypass for loopback,
      - preflight probe,
      - long timeouts + retries + backoff,
      - accurate errors (no hardcoded localhost lines).
    Compatible with .generate(prompt) usage in your code.
    """

    def __init__(self, model: str, timeout_sec: int = 600, retries: int = 5, backoff: float = 2.0):
        # Ensure loopback never goes through a proxy
        os.environ.setdefault("NO_PROXY", "localhost,127.0.0.1")

        self.host = _get_host()
        self.model = model
        self.timeout = int(timeout_sec)
        self.retries = int(retries)
        self.backoff = float(backoff)

        # Fail fast if unreachable (precise message)
        _preflight_probe(self.host, timeout=10)

    def generate(self, prompt: str, **options) -> str:
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        if options:
            payload["options"] = options  # e.g., num_predict, temperature, top_p

        last_err = None
        for attempt in range(self.retries):
            try:
                resp = requests.post(url, json=payload, timeout=self.timeout)
                resp.raise_for_status()
                data = resp.json()
                return data.get("response", "")
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
                last_err = e
                if attempt < self.retries - 1:
                    time.sleep(self.backoff ** (attempt + 1))
                else:
                    raise RuntimeError(
                        f"Ollama call timed out/failed after {self.retries} attempts to {url}: {e!r}"
                    ) from e
            except Exception as e:
                raise RuntimeError(f"Ollama call error to {url}: {e!r}") from e

        raise RuntimeError(f"Ollama call failed: {last_err!r}")