import os
import requests
import json
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key, model, base_url="https://api.openai.com/v1"):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url

    def generate(self, prompt: str) -> str:
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}]
            }
            response = requests.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if 'choices' in data and len(data['choices']) > 0:
                return data['choices'][0]['message']['content']
            elif 'error' in data:
                return f"Error from LLM Provider: {data['error'].get('message', 'Unknown error')}"
            else:
                return f"Unexpected response format: {json.dumps(data)}"
        except Exception as e:
            return f"Failed to generate response from OpenAI: {str(e)}"

class OllamaProvider(LLMProvider):
    def __init__(self, host, model):
        self.host = host
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            payload = {"model": self.model, "prompt": prompt, "stream": False}
            response = requests.post(f"{self.host}/api/generate", json=payload)
            response.raise_for_status()
            data = response.json()
            return data.get('response', f"Unexpected response format: {json.dumps(data)}")
        except Exception as e:
            return f"Failed to generate response from Ollama: {str(e)}"

class AzureOpenAIProvider(LLMProvider):
    def __init__(self, endpoint, api_key, deployment_name):
        self.endpoint = endpoint
        self.api_key = api_key
        self.deployment_name = deployment_name

    def generate(self, prompt: str) -> str:
        try:
            headers = {"api-key": self.api_key, "Content-Type": "application/json"}
            url = f"{self.endpoint}/openai/deployments/{self.deployment_name}/chat/completions?api-version=2023-05-15"
            payload = {"messages": [{"role": "user", "content": prompt}]}
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            if 'choices' in data and len(data['choices']) > 0:
                return data['choices'][0]['message']['content']
            else:
                return f"Unexpected response format from Azure: {json.dumps(data)}"
        except Exception as e:
            return f"Failed to generate response from Azure OpenAI: {str(e)}"

class LLMFactory:
    @staticmethod
    def get_provider(config: dict) -> LLMProvider:
        provider_type = config.get('provider', 'openai').lower()
        if provider_type == 'openai':
            return OpenAIProvider(config.get('api_key'), config.get('model'), config.get('base_url'))
        elif provider_type == 'ollama':
            return OllamaProvider(config.get('ollama', {}).get('host'), config.get('model'))
        elif provider_type == 'azure':
            return AzureOpenAIProvider(config.get('azure', {}).get('endpoint'), config.get('api_key'), config.get('azure', {}).get('deployment_name'))
        else:
            raise ValueError(f"Unsupported LLM provider: {provider_type}")
