import sys
import os
from ai.ai_executor import AIExecutor

def main():
    if len(sys.argv) < 3:
        print("Usage: python ai_quick_fix.py <file_path> <error_message>")
        sys.exit(1)

    file_path = sys.argv[1]
    error_message = " ".join(sys.argv[2:])

    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        sys.exit(1)

    print(f"Analyzing error in {file_path}...")
    executor = AIExecutor()
    fix = executor.get_quick_fix(file_path, error_message)
    
    print("\n--- AI QUICK FIX SUGGESTION ---")
    print(fix)
    print("-------------------------------\n")

if __name__ == "__main__":
    main()
