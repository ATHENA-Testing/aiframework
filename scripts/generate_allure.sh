#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Define Allure results and report directories
ALLURE_RESULTS_DIR="reports/allure-results"
ALLURE_REPORT_DIR="reports/allure-html"

# Check if Allure results exist
if [ ! -d "$ALLURE_RESULTS_DIR" ]; then
  echo "Allure results directory not found: $ALLURE_RESULTS_DIR"
  echo "Please run tests first using run_bdd.sh"
  exit 1
fi

echo "Generating Allure report..."
# Generate Allure report
allure generate "$ALLURE_RESULTS_DIR" --clean -o "$ALLURE_REPORT_DIR"

echo "Allure report generated in $ALLURE_REPORT_DIR"
echo "To view the report, run: allure serve $ALLURE_REPORT_DIR"
