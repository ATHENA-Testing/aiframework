@echo off
setlocal enabledelayedexpansion

echo Starting AI Intelligent Automation Engine...
echo --------------------------------------------------
echo 1. Processing Requirements (requirements\*.txt -^> features\*.feature)
echo 2. Synchronizing Features (features\*.feature -^> steps ^& pages)
echo 3. Processing Smart Prompts (# AI: [prompt] in pages\*.py)
echo 4. Leveraging BasePage Reusable Methods
echo 5. Multi-Model Routing (OpenAI/Gemini/Groq)
echo --------------------------------------------------

set PYTHONPATH=%PYTHONPATH%;.
python ai\ai_generator.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] AI Generation failed. 
    echo Please check your config\ai.yaml and API keys.
    echo You can use scripts\ai_quick_fix.bat to debug specific errors.
) else (
    echo.
    echo --------------------------------------------------
    echo AI Processing complete.
    echo Please review the generated code in pages\ and features\steps\.
)

pause
