import os
import re
import ast
import glob
import yaml
from ai.ai_executor import AIExecutor
from ai.prompt_library import PromptLibrary
from ai.rag_engine import RAGEngine

class AICodeGenerator:
    def __init__(self):
        self.executor = AIExecutor()
        self.prompt_lib = PromptLibrary()
        self.rag = RAGEngine()
        with open("config/ai.yaml", 'r') as f:
            self.ai_config = yaml.safe_load(f)['ai']

    def get_existing_methods(self, directory="pages"):
        methods = []
        for file in glob.glob(f"{directory}/*.py"):
            with open(file, 'r') as f:
                try:
                    tree = ast.parse(f.read())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            methods.append(node.name)
                except SyntaxError:
                    continue
        return list(set(methods))

    def get_step_definitions_map(self, directory="features/steps"):
        step_map = {}
        for file in glob.glob(f"{directory}/*.py"):
            with open(file, 'r') as f:
                content = f.read()
                pattern = r'(@(?:given|when|then)\(.*?\)[\s\S]*?def\s+\w+\(context.*?\):[\s\S]*?)(?=\n@|\ndef|\Z)'
                matches = re.findall(pattern, content)
                for code_block in matches:
                    text_match = re.search(r'@(?:given|when|then)\([\'"](.*?)[\'"]\)', code_block)
                    if text_match:
                        step_text = text_match.group(1)
                        step_map[step_text] = (file, code_block.strip())
        return step_map

    def append_to_file(self, file_path, code):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write("from behave import given, when, then\n" if "steps" in file_path else "")
        
        with open(file_path, 'a') as f:
            f.write("\n" + code + "\n")

    def sync_feature_to_code(self, feature_path):
        print(f"Syncing feature: {feature_path}")
        with open(feature_path, 'r') as f:
            lines = f.readlines()

        feature_name = os.path.basename(feature_path).replace('.feature', '')
        target_page = f"pages/{feature_name}_page.py"
        target_steps = f"features/steps/{feature_name}_steps.py"
        
        step_map = self.get_step_definitions_map()

        for line in lines:
            line = line.strip()
            if any(line.startswith(kw) for kw in ['Given', 'When', 'Then']):
                step_text = re.sub(r'^(Given|When|Then)\s+', '', line)
                
                if step_text not in step_map:
                    print(f"Detected new/updated step: {step_text}")
                    
                    # RAG Context for Page Method
                    rag_context = self.rag.query(step_text)
                    
                    # 1. Generate/Update Page Method
                    existing_methods = self.get_existing_methods()
                    page_prompt = self.prompt_lib.PAGE_METHOD_GENERATION_PROMPT.format(
                        rag_context=rag_context,
                        existing_methods=", ".join(existing_methods),
                        action_description=f"Perform action for: {step_text}"
                    )
                    page_code = self.executor.provider.generate(page_prompt).strip()
                    page_code = re.sub(r'```python|```', '', page_code).strip()
                    
                    if "# Use existing method" not in page_code and page_code:
                        self.append_to_file(target_page, page_code)

                    # 2. Generate Step Definition
                    step_prompt = self.prompt_lib.STEP_DEFINITION_GENERATION_PROMPT.format(
                        step_text=line,
                        existing_steps=", ".join(step_map.keys()),
                        page_methods=", ".join(self.get_existing_methods())
                    )
                    step_code = self.executor.provider.generate(step_prompt).strip()
                    step_code = re.sub(r'```python|```', '', step_code).strip()
                    
                    if "# Step already exists" not in step_code and step_code:
                        self.append_to_file(target_steps, step_code)

    def process_smart_prompts(self, directory="pages"):
        for file in glob.glob(f"{directory}/*.py"):
            with open(file, 'r') as f:
                content = f.read()
            
            prompts = re.findall(r'# AI: (.*)', content)
            if not prompts:
                continue
            
            print(f"Processing smart prompts in {file}...")
            for prompt_text in prompts:
                # RAG Context for logic generation
                rag_context = self.rag.query(prompt_text)
                
                existing_methods = self.get_existing_methods()
                ai_prompt = self.prompt_lib.LOGIC_GENERATION_PROMPT.format(
                    user_prompt=prompt_text + f"\nContext from knowledge base: {rag_context}",
                    existing_methods=", ".join(existing_methods)
                )
                generated_code = self.executor.provider.generate(ai_prompt).strip()
                generated_code = re.sub(r'```python|```', '', generated_code).strip()
                
                full_prompt_line = f"# AI: {prompt_text}"
                content = content.replace(full_prompt_line, generated_code)
            
            with open(file, 'w') as f:
                f.write(content)

    def generate_feature_from_requirement(self, requirement_path):
        if not self.executor.enabled:
            return None
        with open(requirement_path, 'r') as f:
            req_text = f.read()
        
        # RAG Context for Feature generation
        rag_context = self.rag.query(req_text)
        
        prompt = self.prompt_lib.FEATURE_GENERATION_PROMPT.format(
            rag_context=rag_context,
            requirement_text=req_text
        )
        feature_content = self.executor.provider.generate(prompt).strip()
        feature_content = re.sub(r'```gherkin|```', '', feature_content).strip()
        base_name = os.path.basename(requirement_path).replace('.txt', '.feature')
        feature_path = f"features/{base_name}"
        with open(feature_path, 'w') as f:
            f.write(feature_content)
        return feature_path

    def process_all(self):
        # 0. Rebuild RAG Index
        self.rag.rebuild_index()
        
        # 1. Requirements to Features
        req_files = glob.glob("requirements/*.txt")
        for req in req_files:
            self.generate_feature_from_requirement(req)
        
        # 2. Features to Code (Sync)
        feature_files = glob.glob("features/*.feature")
        for feature in feature_files:
            self.sync_feature_to_code(feature)
            
        # 3. In-code Smart Prompts
        self.process_smart_prompts()

if __name__ == "__main__":
    generator = AICodeGenerator()
    generator.process_all()
