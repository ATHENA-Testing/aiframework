@echo off
set ALLURE_RESULTS_DIR=reports\allure-results
set ALLURE_REPORT_DIR=reports\allure-html

if not exist "%ALLURE_RESULTS_DIR%" (
    echo Allure results directory not found: %ALLURE_RESULTS_DIR%
    echo Please run tests first using run_bdd.bat
    pause
    exit /b 1
)

echo Generating Allure report...
allure generate "%ALLURE_RESULTS_DIR%" --clean -o "%ALLURE_REPORT_DIR%"

echo Allure report generated in %ALLURE_REPORT_DIR%
echo To view the report, run: allure serve %ALLURE_REPORT_DIR%
pause
