@echo off
setlocal

echo Starting AI Intelligent Automation Engine...

REM --- Optional /restart: kill existing listener on 11434 ---
if /i "%~1"=="/restart" (
  for /f "tokens=5" %%A in ('netstat -ano ^| findstr ":11434" ^| findstr LISTENING') do set "PID=%%A"
  if defined PID (
    echo Restart requested. Killing PID %PID% ...
    taskkill /PID %PID% /F >nul 2>&1
    timeout /t 2 >nul
  ) else (
    echo Restart requested but nothing is listening on 11434.
  )
)

REM --- Start Ollama if not already listening ---
set "PID="
for /f "tokens=5" %%A in ('netstat -ano ^| findstr ":11434" ^| findstr LISTENING') do set "PID=%%A"

if not defined PID (
  echo Ollama not running. Starting...
  start "" /min ollama serve
  timeout /t 5 >nul
) else (
  echo Ollama already running on PID %PID%.
)

REM --- Probe via PowerShell script (no proxy, retries) ---
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0ollama_probe.ps1"
if errorlevel 1 (
  echo ERROR: Ollama API unreachable after retries.
  echo Tip: scripts\ai_generate.bat /restart
  exit /b 1
)

echo Ollama API OK.

REM --- Warmup (preload model for faster first token) ---
echo Warming up model...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0ollama_warmup.ps1" -Model "llama2:latest"

echo --------------------------------------------------
echo 1. Processing Requirements (requirements*.txt -^> features*.feature)
echo 2. Synchronizing Features (features*.feature -^> steps ^& pages)
echo 3. Processing Smart Prompts (# AI: [prompt] in pages*.py)
echo 4. Leveraging BasePage Reusable Methods
echo 5. Multi-Model Routing (OpenAI/Gemini/Groq)
echo --------------------------------------------------

REM --- Ensure Python requests do not route localhost via a proxy ---
set "NO_PROXY=localhost,127.0.0.1"

REM --- Tell Python client the host to use explicitly (prefer 127.0.0.1 over localhost) ---
set "OLLAMA_HOST=http://127.0.0.1:11434"

REM --- Ensure project root is on PYTHONPATH (do NOT overwrite it with a URL) ---
set "PYTHONPATH=%PYTHONPATH%;."

REM --- Run your Python generator as a package module (stable imports) ---
python -m ai.ai_generator

if %ERRORLEVEL% NEQ 0 (
  echo.
  echo [ERROR] AI Generation failed.
  echo Please check config\ai.yaml, model routing, and API keys.
  echo Tip: use scripts\ai_generate.bat /restart to restart local Ollama cleanly.
) else (
  echo.
  echo --------------------------------------------------
  echo AI Processing complete.
  echo Please review the generated code in pages\ and features\steps\.
)

endlocal
exit /b 0