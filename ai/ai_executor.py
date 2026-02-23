import yaml
import os
from ai.llm_provider import LLMFactory
from ai.prompt_library import PromptLibrary

class AIExecutor:
    def __init__(self, config_path="config/ai.yaml"):
        self.config = self._load_config(config_path)
        self.enabled = self.config.get('enabled', False)
        self.mode = self.config.get('mode', 'off')
        self.routing = self.config.get('routing', {})
        if self.enabled:
            self.provider = LLMFactory.get_provider(self.config)
        else:
            self.provider = None

    def _load_config(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                return yaml.safe_load(f).get('ai', {})
        return {}

    def _get_provider_for_task(self, task_type):
        """Returns the provider based on routing configuration or default."""
        if not self.enabled:
            return None
        
        provider_name = self.routing.get(task_type)
        if provider_name:
            temp_config = self.config.copy()
            temp_config['provider'] = provider_name
            if provider_name in self.config:
                temp_config.update(self.config[provider_name])
            return LLMFactory.get_provider(temp_config)
        
        return self.provider

    def execute_review(self, code: str) -> str:
        if not self.enabled or self.mode not in ['review', 'generate']:
            return "AI Review is disabled or mode not set to review."
        
        provider = self._get_provider_for_task('review')
        prompt = PromptLibrary.CODE_REVIEW_PROMPT.format(code=code)
        return provider.generate(prompt)

    def execute_assert(self, condition: str, context_data: str) -> str:
        if not self.enabled:
            return "AI is disabled."
        
        provider = self._get_provider_for_task('assertion')
        prompt = f"Act as a QA Engineer. Verify the following condition: {condition}. Context: {context_data}. Return 'PASS' or 'FAIL' with a brief reason."
        return provider.generate(prompt)

    def suggest_method(self, description: str) -> str:
        if not self.enabled or self.mode not in ['assist', 'generate']:
            return "AI Assistance is disabled."
        
        prompt = PromptLibrary.METHOD_SUGGESTION_PROMPT.format(description=description)
        return self.provider.generate(prompt)

    def generate_steps(self, feature_text: str) -> str:
        if not self.enabled or self.mode != 'generate':
            return "AI Generation is disabled."
        
        prompt = PromptLibrary.STEP_GENERATION_PROMPT.format(feature_text=feature_text)
        return self.provider.generate(prompt)

    def get_quick_fix(self, file_path: str, error_message: str) -> str:
        if not self.enabled:
            return "AI is disabled."
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return f"Failed to read file for quick fix: {str(e)}"
            
        prompt = PromptLibrary.QUICK_FIX_PROMPT.format(
            file_path=file_path,
            error_message=error_message,
            file_content=content
        )
        return self.provider.generate(prompt)
