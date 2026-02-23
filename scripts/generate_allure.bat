@echo off
setlocal enabledelayedexpansion

set ALLURE_RESULTS_DIR=reports\allure-results
set ALLURE_REPORT_DIR=reports\allure-html

if not exist "%ALLURE_RESULTS_DIR%" (
    echo.
    echo [ERROR] Allure results directory not found: %ALLURE_RESULTS_DIR%
    echo Please run tests first using scripts\run_bdd.bat
    echo.
    pause
    exit /b 1
)

echo Generating Allure report...
echo --------------------------------------------------
echo Source: %ALLURE_RESULTS_DIR%
echo Output: %ALLURE_REPORT_DIR%
echo --------------------------------------------------

allure generate "%ALLURE_RESULTS_DIR%" --clean -o "%ALLURE_REPORT_DIR%"

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Allure report generation failed. 
    echo Please ensure Allure is installed and in your PATH.
) else (
    echo.
    echo --------------------------------------------------
    echo Allure report generated in %ALLURE_REPORT_DIR%
    echo To view the report, run: allure open %ALLURE_REPORT_DIR%
    echo Or to serve locally: allure serve %ALLURE_RESULTS_DIR%
)

pause
