import requests
import json
import os
import time

class LLMProvider:
    def generate(self, prompt: str) -> str:
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key, model, base_url="https://api.openai.com/v1"):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        if base_url and "your_api_key_here" not in base_url:
            self.base_url = base_url
        else:
            self.base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

    def generate(self, prompt: str) -> str:
        max_retries = 3
        retry_delay = 2
        models_to_try = [self.model, "gpt-4o-mini", "gpt-3.5-turbo"]
        models_to_try = list(dict.fromkeys([m for m in models_to_try if m]))

        last_error = "Unknown error"
        for model in models_to_try:
            for attempt in range(max_retries):
                try:
                    headers = {"Authorization": f"Bearer {self.api_key}"}
                    payload = {
                        "model": model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7
                    }
                    response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=30)
                    
                    if response.status_code == 429:
                        last_error = f"Rate limit reached for model {model}"
                        if attempt < max_retries - 1:
                            time.sleep(retry_delay * (2 ** attempt))
                            continue
                        else:
                            break
                            
                    response.raise_for_status()
                    data = response.json()
                    if 'choices' in data and len(data['choices']) > 0:
                        return data['choices'][0]['message']['content']
                    else:
                        last_error = f"Unexpected response format from {model}: {json.dumps(data)}"
                        break
                except Exception as e:
                    last_error = str(e)
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        continue
                    break
        
        return f"Failed to generate response from OpenAI after trying multiple models and retries. Last error: {last_error}"

class GeminiProvider(LLMProvider):
    def __init__(self, api_key, model="gemini-1.5-flash"):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    def generate(self, prompt: str) -> str:
        try:
            url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            return f"Failed to generate response from Gemini: {str(e)}"

class GroqProvider(LLMProvider):
    def __init__(self, api_key, model="llama3-8b-8192"):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
        self.model = model
        self.base_url = "https://api.groq.com/openai/v1"

    def generate(self, prompt: str) -> str:
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}]
            }
            response = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content']
        except Exception as e:
            return f"Failed to generate response from Groq: {str(e)}"

class OllamaProvider(LLMProvider):
    def __init__(self, host, model):
        self.host = host.rstrip('/') if host else "http://localhost:11434"
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            payload = {"model": self.model, "prompt": prompt, "stream": False}
            url = f"{self.host}/api/generate"
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 404:
                return f"Error: Ollama endpoint not found at {url}. Please ensure Ollama is running."
            response.raise_for_status()
            data = response.json()
            return data.get('response', f"Unexpected response format: {json.dumps(data)}")
        except requests.exceptions.ConnectionError:
            return f"Error: Could not connect to Ollama at {self.host}. Is it running?"
        except Exception as e:
            return f"Failed to generate response from Ollama: {str(e)}"

class AzureOpenAIProvider(LLMProvider):
    def __init__(self, endpoint, api_key, deployment_name):
        self.endpoint = endpoint
        self.api_key = api_key
        self.deployment_name = deployment_name

    def generate(self, prompt: str) -> str:
        try:
            headers = {"Content-Type": "application/json", "api-key": self.api_key}
            payload = {"messages": [{"role": "user", "content": prompt}], "max_tokens": 2000}
            url = f"{self.endpoint}/openai/deployments/{self.deployment_name}/chat/completions?api-version=2023-05-15"
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data['choices'][0]['message']['content']
        except Exception as e:
            return f"Failed to generate response from Azure OpenAI: {str(e)}"

class LLMFactory:
    @staticmethod
    def get_provider(config):
        provider_type = config.get('provider', 'openai').lower()
        if provider_type == 'openai':
            return OpenAIProvider(
                api_key=config.get('api_key'),
                model=config.get('model', 'gpt-4o-mini'),
                base_url=config.get('base_url', 'https://api.openai.com/v1')
            )
        elif provider_type == 'gemini':
            return GeminiProvider(
                api_key=config.get('api_key'),
                model=config.get('model', 'gemini-1.5-flash')
            )
        elif provider_type == 'groq':
            return GroqProvider(
                api_key=config.get('api_key'),
                model=config.get('model', 'llama3-8b-8192')
            )
        elif provider_type == 'ollama':
            return OllamaProvider(
                host=config.get('ollama', {}).get('host', 'http://localhost:11434'),
                model=config.get('model', 'llama2')
            )
        elif provider_type == 'azure':
            azure_config = config.get('azure', {})
            return AzureOpenAIProvider(
                endpoint=azure_config.get('endpoint'),
                api_key=config.get('api_key'),
                deployment_name=azure_config.get('deployment_name')
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider_type}")
