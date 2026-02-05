#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Define Allure results directory
ALLURE_RESULTS_DIR="reports/allure-results"

# Create Allure results directory if it doesn't exist
mkdir -p "$ALLURE_RESULTS_DIR"

echo "Running Behave tests..."
# Run Behave tests and generate Allure results
behave -f allure_behave.formatter:AllureFormatter -o "$ALLURE_RESULTS_DIR" features/

echo "Behave tests finished. Allure results generated in $ALLURE_RESULTS_DIR"
