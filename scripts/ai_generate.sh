#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting AI Intelligent Automation Engine..."
echo "--------------------------------------------------"
echo "1. Processing Requirements (requirements/*.txt -> features/*.feature)"
echo "2. Synchronizing Features (features/*.feature -> steps & pages)"
echo "3. Processing Smart Prompts (# AI: [prompt] in pages/*.py)"

# Run the AI Code Generator
python3 -m ai.ai_generator

echo "--------------------------------------------------"
echo "AI Processing complete."
echo "Summary of Changes:"
echo "- New features generated from requirements."
echo "- Existing step definitions updated for modified features."
echo "- Smart Prompts in Page Classes replaced with Selenium logic."
echo "--------------------------------------------------"
echo "Please review the generated code in pages/ and features/steps/."
