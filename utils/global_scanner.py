import os
import glob
import re
import ast

class GlobalScanner:
    @staticmethod
    def get_all_feature_steps(directory="features"):
        steps = []
        pattern = os.path.join(directory, "**", "*.feature")
        for file in glob.glob(pattern, recursive=True):
            with open(file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if any(line.startswith(kw) for kw in ['Given', 'When', 'Then', 'And', 'But']):
                        # Normalize step text by removing the keyword
                        step_text = re.sub(r'^(Given|When|Then|And|But)\s+', '', line)
                        steps.append(step_text)
        return list(set(steps))

    @staticmethod
    def get_all_step_definitions(directory="features/steps"):
        step_defs = {}
        pattern = os.path.join(directory, "**", "*.py")
        for file in glob.glob(pattern, recursive=True):
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Match @given('text'), @when("text"), etc.
                matches = re.findall(r'@(?:given|when|then)\([\'"](.*?)[\'"]\)', content)
                for step_text in matches:
                    step_defs[step_text] = file
        return step_defs

    @staticmethod
    def get_all_page_methods(directory="pages"):
        methods = {}
        pattern = os.path.join(directory, "**", "*.py")
        for file in glob.glob(pattern, recursive=True):
            with open(file, 'r', encoding='utf-8') as f:
                try:
                    tree = ast.parse(f.read())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef):
                            if node.name != "__init__":
                                methods[node.name] = file
                except SyntaxError:
                    continue
        return methods
