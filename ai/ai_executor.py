import yaml
import os
from ai.llm_provider import LLMFactory
from ai.prompt_library import PromptLibrary

class AIExecutor:
    def __init__(self, config_path="config/ai.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)['ai']
        
        self.enabled = self.config.get('enabled', False)
        self.mode = self.config.get('mode', 'off')
        
        if self.enabled and self.mode != 'off':
            self.provider = LLMFactory.get_provider(self.config)
        else:
            self.provider = None

    def execute_review(self, code: str) -> str:
        if not self.enabled or self.mode not in ['review', 'generate']:
            return "AI Review is disabled or mode not set to review."
        
        prompt = PromptLibrary.CODE_REVIEW_PROMPT.format(code=code)
        return self.provider.generate(prompt)

    def execute_assert(self, condition: str, context_data: str) -> str:
        if not self.enabled:
            return "AI is disabled."
        
        prompt = f"Act as a QA Engineer. Verify the following condition: {condition}. Context: {context_data}. Return 'PASS' or 'FAIL' with a brief reason."
        return self.provider.generate(prompt)

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
