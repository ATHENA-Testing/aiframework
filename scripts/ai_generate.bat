@echo off
echo Starting AI Intelligent Automation Engine...
echo --------------------------------------------------
echo 1. Processing Requirements (requirements\*.txt -^> features\*.feature)
echo 2. Synchronizing Features (features\*.feature -^> steps ^& pages)
echo 3. Processing Smart Prompts (# AI: [prompt] in pages\*.py)

python -m ai.ai_generator

echo --------------------------------------------------
echo AI Processing complete.
echo Please review the generated code in pages\ and features\steps\.
pause
