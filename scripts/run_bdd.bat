@echo off
set ALLURE_RESULTS_DIR=reports\allure-results

if not exist "%ALLURE_RESULTS_DIR%" mkdir "%ALLURE_RESULTS_DIR%"

echo Running Behave tests...
behave -f allure_behave.formatter:AllureFormatter -o "%ALLURE_RESULTS_DIR%" features\

echo Behave tests finished. Allure results generated in %ALLURE_RESULTS_DIR%
pause
