#!/bin/bash

# Auth0 Configuration
export AUTH0_DOMAIN='udacity-cofshp.us.auth0.com'
export SECRET_KEY='this-is-a-secret-key-for-local-development-only'
export JWT_SECRET_KEY='this-is-a-jwt-secret-key-for-local-development-only'
export API_AUDIENCE='https://securityapp/'
export API_IDENTIFIER='https://securityapp/'
export AUTH0_CLIENT_ID='dYfY9fLTPlgVE3kgXuHQFGKLp7MfxgyH'

# Database Configuration
export DATABASE_URL='postgresql://postgres:newpassword@localhost:5432/postgres'
export TEST_DATABASE_URL='postgresql://postgres:newpassword@localhost:5432/postgres_test'

# Flask Configuration
export FLASK_APP=app.py
export FLASK_ENV=development

echo "Environment variables set successfully!"
echo "SECRET_KEY: [HIDDEN]"
echo "JWT_SECRET_KEY: [HIDDEN]"
echo "AUTH0_DOMAIN: $AUTH0_DOMAIN"
echo "API_AUDIENCE: $API_AUDIENCE"
echo "API_IDENTIFIER: $API_IDENTIFIER"
echo "AUTH0_CLIENT_ID: $AUTH0_CLIENT_ID"
echo "DATABASE_URL: $DATABASE_URL"
echo "TEST_DATABASE_URL: $TEST_DATABASE_URL"

# Instructions for use
echo ""
echo "To use these environment variables, run:"
echo "source setup.sh"
echo ""
echo "To obtain tokens for testing, use the following roles and permissions:"
echo "1. Tool Viewer: read:tools"
echo "2. Tool Editor: read:tools, update:tools"
echo "3. Tool Admin: read:tools, create:tools, update:tools, delete:tools"
