import os
import glob
from ai.ai_executor import AIExecutor

class AICodeReviewer:
    def __init__(self):
        self.executor = AIExecutor()

    def review_project(self):
        if not self.executor.enabled:
            print("AI is disabled in config/ai.yaml")
            return

        print("Starting AI Code Review...")
        review_content = "# AI Project Code Review\n\n"
        
        # Review files in pages/ and features/steps/
        files_to_review = glob.glob("pages/*.py") + glob.glob("features/steps/*.py")
        
        for file_path in files_to_review:
            print(f"Reviewing {file_path}...")
            with open(file_path, 'r') as f:
                code = f.read()
            
            review = self.executor.execute_review(code)
            review_content += f"## Review for {file_path}\n\n{review}\n\n"

        os.makedirs("review", exist_ok=True)
        with open("review/ai_review_report.md", "w") as f:
            f.write(review_content)
        
        print("Review complete. Report saved to review/ai_review_report.md")

if __name__ == "__main__":
    reviewer = AICodeReviewer()
    reviewer.review_project()

def main():
    reviewer = AICodeReviewer()
    reviewer.review_project()

if __name__ == "__main__":
    main()
