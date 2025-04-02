#!/bin/bash

# Cybersecurity Tools Management API Testing Script
# This script automates some of the testing steps from the TESTING_GUIDE.md

echo "===== Cybersecurity Tools Management API Testing Script ====="
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Virtual environment is not activated. Please activate it first:"
    echo "source venv/bin/activate"
    exit 1
fi

# Set up environment variables
echo "Setting up environment variables..."
source setup.sh
echo "Environment variables set."
echo ""

# Test database connection
echo "Testing database connection..."
python tests/test_postgres_db.py
if [ $? -ne 0 ]; then
    echo "Database connection test failed. Please check your database configuration."
    exit 1
fi
echo "Database connection test passed."
echo ""

# Run automated tests
echo "Running automated tests..."
echo ""

echo "1. Running basic tests (test_app.py)..."
python -m unittest tests/test_app.py
if [ $? -ne 0 ]; then
    echo "Basic tests failed. Please check the errors above."
    exit 1
fi
echo "Basic tests passed."
echo ""

echo "2. Running comprehensive tests with RBAC (test_app_new.py)..."
python -m unittest tests/test_app_new.py
if [ $? -ne 0 ]; then
    echo "RBAC tests failed. Please check the errors above."
    exit 1
fi
echo "RBAC tests passed."
echo ""

echo "3. Running all tests..."
python -m unittest discover -s tests
if [ $? -ne 0 ]; then
    echo "Some tests failed. Please check the errors above."
    exit 1
fi
echo "All tests passed."
echo ""

echo "===== Testing completed successfully! ====="
echo ""
echo "Next steps:"
echo "1. Start the Flask application: flask run"
echo "2. Perform manual API testing as described in TESTING_GUIDE.md"
echo "3. Test deployment to Render if needed"
echo ""
echo "For detailed testing instructions, please refer to TESTING_GUIDE.md"
