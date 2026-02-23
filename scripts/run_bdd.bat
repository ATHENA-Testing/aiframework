@echo off
setlocal enabledelayedexpansion

set ALLURE_RESULTS_DIR=reports\allure-results
if not exist "%ALLURE_RESULTS_DIR%" mkdir "%ALLURE_RESULTS_DIR%"

echo Running Behave tests...
echo --------------------------------------------------
echo Target: features\
echo Results: %ALLURE_RESULTS_DIR%
echo --------------------------------------------------

set PYTHONPATH=%PYTHONPATH%;.
behave -f allure_behave.formatter:AllureFormatter -o "%ALLURE_RESULTS_DIR%" features\

if %ERRORLEVEL% neq 0 (
    echo.
    echo [WARNING] Some tests failed. 
    echo Check the Allure report for details.
    echo Use scripts\ai_quick_fix.bat to debug specific failures.
) else (
    echo.
    echo --------------------------------------------------
    echo Behave tests finished successfully.
)

pause
