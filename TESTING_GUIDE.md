# Cybersecurity Tools Management API - Testing Guide

This guide provides comprehensive instructions for testing the Cybersecurity Tools Management API to ensure all functionality is working correctly before submission.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setting Up the Testing Environment](#setting-up-the-testing-environment)
3. [Database Testing](#database-testing)
4. [Manual API Testing](#manual-api-testing)
5. [Authentication Testing](#authentication-testing)
6. [Automated Testing](#automated-testing)
7. [Deployment Testing](#deployment-testing)
8. [Final Checklist](#final-checklist)

## Prerequisites

Before starting the testing process, ensure you have the following:

- Python 3.8 or later installed
- PostgreSQL installed and running
- Git installed
- Postman or cURL for API testing
- Auth0 account set up (as described in README.md)
- Render account (for deployment testing)

## Setting Up the Testing Environment

1. **Clone the repository (if not already done)**:
   ```bash
   git clone https://github.com/krillavilla/Cybersecurity_Tools_Management_API.git
   cd Cybersecurity_Tools_Management_API
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   source setup.sh
   ```

   Verify that the environment variables are set correctly:
   ```bash
   echo $AUTH0_DOMAIN
   echo $API_AUDIENCE
   echo $DATABASE_URL
   ```

## Database Testing

1. **Test database connection**:
   ```bash
   python tests/test_postgres_db.py
   ```

   Expected output:
   ```
   Connected to the database successfully!
   ```

2. **Initialize the database**:
   ```bash
   flask db upgrade
   ```

   This should create all necessary tables in your database.

3. **Verify database tables**:
   Connect to your PostgreSQL database and check if the tables are created:
   ```bash
   psql postgresql://postgres:newpassword@localhost:5432/postgres
   \dt
   ```

   You should see the `tool` and `user` tables listed.

4. **Populate the database with sample data**:
   ```bash
   python populate_db.py
   ```

   This script will create sample users and tools in the database for testing purposes. The output should indicate that users and tools were created successfully.

## Manual API Testing

Use Postman or cURL to test the API endpoints manually. You'll need valid tokens for each role (Tool Viewer, Tool Editor, Tool Admin).

1. **Start the application**:
   ```bash
   flask run
   ```

2. **Test the home endpoint**:
   ```bash
   curl http://127.0.0.1:5000/
   ```

   Expected response:
   ```json
   {"message":"Welcome to the Cybersecurity Tools Management API!"}
   ```

3. **Test GET /api/tools endpoint (requires authentication)**:
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" http://127.0.0.1:5000/api/tools
   ```

   Replace `YOUR_TOKEN` with a valid token for any role.

   Expected response format:
   ```json
   {
     "success": true,
     "tools": [...]
   }
   ```

4. **Test POST /api/tools endpoint (requires Tool Admin role)**:
   ```bash
   curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer ADMIN_TOKEN" -d '{"name":"Test Tool", "description":"A test tool", "user_id":1}' http://127.0.0.1:5000/api/tools
   ```

   Replace `ADMIN_TOKEN` with a valid token for the Tool Admin role.

   Expected response format:
   ```json
   {
     "success": true,
     "tool": {...}
   }
   ```

5. **Test PATCH /api/tools/:id endpoint (requires Tool Editor or Admin role)**:
   ```bash
   curl -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer EDITOR_TOKEN" -d '{"name":"Updated Tool"}' http://127.0.0.1:5000/api/tools/1
   ```

   Replace `EDITOR_TOKEN` with a valid token for the Tool Editor or Tool Admin role.

   Expected response format:
   ```json
   {
     "success": true,
     "tool": {...}
   }
   ```

6. **Test DELETE /api/tools/:id endpoint (requires Tool Admin role)**:
   ```bash
   curl -X DELETE -H "Authorization: Bearer ADMIN_TOKEN" http://127.0.0.1:5000/api/tools/1
   ```

   Replace `ADMIN_TOKEN` with a valid token for the Tool Admin role.

   Expected response format:
   ```json
   {
     "success": true,
     "deleted": 1
   }
   ```

7. **Test GET /api/users endpoint (requires authentication)**:
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" http://127.0.0.1:5000/api/users
   ```

   Replace `YOUR_TOKEN` with a valid token for any role.

   Expected response format:
   ```json
   {
     "success": true,
     "users": [...]
   }
   ```

## Authentication Testing

### Obtaining a Token

You can use the provided script to obtain a valid token for testing:

```bash
python sending_token_API.py
```

This script will return a JSON response containing an access token that you can use for testing the API endpoints. The token will have the necessary permissions based on the client credentials used.

For detailed instructions on obtaining tokens and troubleshooting authentication issues, refer to the [Authentication Guide](AUTH_GUIDE.md).

### Testing with Different Roles

1. **Test with Tool Viewer role**:
   - Should be able to access GET /api/tools
   - Should NOT be able to create, update, or delete tools

2. **Test with Tool Editor role**:
   - Should be able to access GET /api/tools
   - Should be able to update tools (PATCH /api/tools/:id)
   - Should NOT be able to create or delete tools

3. **Test with Tool Admin role**:
   - Should have full access to all endpoints

4. **Test with invalid token**:
   ```bash
   curl -H "Authorization: Bearer INVALID_TOKEN" http://127.0.0.1:5000/api/tools
   ```

   Expected response:
   ```json
   {
     "success": false,
     "error": 401,
     "message": "..."
   }
   ```

5. **Test with missing token**:
   ```bash
   curl http://127.0.0.1:5000/api/tools
   ```

   Expected response:
   ```json
   {
     "success": false,
     "error": 401,
     "message": "Authorization header is expected."
   }
   ```

## Automated Testing

You can run the automated tests manually or use the provided test script:

### Using the Automated Test Script

The repository includes a shell script that automates many of the testing steps:

```bash
# Make the script executable
chmod +x test_api.sh

# Run the script
./test_api.sh
```

This script will:
1. Check if your virtual environment is activated
2. Set up environment variables
3. Test the database connection
4. Run all the automated tests
5. Provide feedback on the results

### Running Tests Manually

If you prefer to run tests manually:

1. **Run the basic test suite**:
   ```bash
   python -m unittest tests/test_app.py
   ```

2. **Run the comprehensive test suite with RBAC tests**:
   ```bash
   python -m unittest tests/test_app_new.py
   ```

3. **Run all tests**:
   ```bash
   python -m unittest discover -s tests
   ```

All tests should pass without errors. If any test fails, investigate and fix the issue before proceeding.

## Deployment Testing

Test the deployment process to ensure the application can be deployed to Render:

1. **Login to Render**:
   - Go to [Render Dashboard](https://dashboard.render.com/) and log in to your account.

2. **Deploy using Blueprint**:
   - Click on "New" and select "Blueprint".
   - Connect your GitHub repository if you haven't already.
   - Select your repository and click "Apply".
   - Render will automatically detect the `render.yaml` file and create the necessary services.

3. **Set environment variables on Render**:
   - After the services are created, go to the web service dashboard.
   - Navigate to **Environment** → **Environment Variables**.
   - Add the following variables:
     - `AUTH0_DOMAIN`: Your Auth0 domain.
     - `API_AUDIENCE`: Your API audience.
     - `API_IDENTIFIER`: Your API identifier.
     - `AUTH0_CLIENT_ID`: Your Auth0 client ID.
     - `AUTH0_CLIENT_SECRET`: Your Auth0 client secret.

4. **Deploy your API**:
   - Click on "Manual Deploy" and select "Deploy latest commit".
   - Wait for the deployment to complete.

5. **Test the deployed API**:
   ```bash
   curl https://cybersecurity-tools-api.onrender.com/
   ```

   Expected response:
   ```json
   {"message":"Welcome to the Cybersecurity Tools Management API!"}
   ```

6. **Test the deployed API with authentication**:
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" https://cybersecurity-tools-api.onrender.com/api/tools
   ```

   Replace `YOUR_TOKEN` with a valid token.

## Final Checklist

Before submitting the project, verify the following:

- [ ] Database connection works
- [ ] Database is populated with sample data
- [ ] All API endpoints return the expected responses
- [ ] Authentication and authorization work correctly for all roles
- [ ] All automated tests pass
- [ ] The application can be deployed to Render
- [ ] The deployed application works correctly
- [ ] The README.md file is complete and accurate
- [ ] The setup.sh file contains all necessary environment variables
- [ ] The requirements.txt file includes all dependencies

## Helpful Scripts

This project includes several scripts to help with testing:

1. **test_api.sh**: Automates the process of running tests
   ```bash
   chmod +x test_api.sh
   ./test_api.sh
   ```

2. **populate_db.py**: Populates the database with sample data
   ```bash
   python populate_db.py
   ```

3. **setup.sh**: Sets up environment variables
   ```bash
   source setup.sh
   ```

If all items on the checklist are verified, the project is ready for submission!
