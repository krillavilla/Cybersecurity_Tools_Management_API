# Authentication Guide for Cybersecurity Tools Management API

This guide provides detailed instructions on how to obtain and use authentication tokens for the Cybersecurity Tools Management API.

## Table of Contents
1. [Understanding Authentication in this API](#understanding-authentication-in-this-api)
2. [Method 1: Using the sending_token_API.py Script](#method-1-using-the-sending_token_apipy-script)
3. [Method 2: Using Auth0 Dashboard](#method-2-using-auth0-dashboard)
4. [Method 3: Using Auth0 Authentication API Directly](#method-3-using-auth0-authentication-api-directly)
5. [Using Tokens in API Requests](#using-tokens-in-api-requests)
6. [Environment Variable Configuration](#environment-variable-configuration)
7. [Troubleshooting](#troubleshooting)

## Understanding Authentication in this API

The Cybersecurity Tools Management API uses Auth0 for authentication and implements Role-Based Access Control (RBAC). There are three roles with different permissions:

1. **Tool Viewer**: Can only view tools
   - Permissions: `read:tools`

2. **Tool Editor**: Can view and edit tools
   - Permissions: `read:tools`, `update:tools`

3. **Tool Admin**: Has full access to tools
   - Permissions: `read:tools`, `create:tools`, `update:tools`, `delete:tools`

To access protected endpoints, you need to obtain a valid JWT token with the appropriate permissions.

## Method 1: Using the sending_token_API.py Script

The easiest way to obtain a token is to use the provided `sending_token_API.py` script. This script uses the client credentials flow to obtain a token from Auth0.

### Prerequisites
- Python 3.8 or later
- The project dependencies installed (`pip install -r requirements.txt`)
- Auth0 client credentials (client ID and client secret)

### Steps

1. **Set up environment variables**:

   You can set the Auth0 credentials in the `.env` file:
   ```
   AUTH0_DOMAIN='udacity-cofshp.us.auth0.com'
   API_AUDIENCE='https://securityapp/'
   AUTH0_CLIENT_ID='your-client-id'
   AUTH0_CLIENT_SECRET='your-client-secret'
   ```

   Or you can use the default values in the script (not recommended for production).

2. **Run the script**:
   ```bash
   python sending_token_API.py
   ```

3. **Copy the token**:
   The script will output a token that you can use for API requests. It will look something like:
   ```
   Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkVxTm1...
   ```

### Notes
- The token obtained using this method will have the permissions associated with the client credentials used.
- By default, the script uses the client credentials flow, which is suitable for machine-to-machine authentication.
- The token will expire after a certain period (typically 24 hours).

## Method 2: Using Auth0 Dashboard

If you need tokens with specific roles and permissions, you can create test users in the Auth0 Dashboard and assign them to roles.

### Prerequisites
- An Auth0 account
- Access to the Auth0 Dashboard

### Steps

1. **Log in to the Auth0 Dashboard**:
   Go to [Auth0 Dashboard](https://manage.auth0.com/) and log in.

2. **Create a new user**:
   - Go to "User Management" > "Users"
   - Click "Create User"
   - Fill in the details and create the user

3. **Assign the user to a role**:
   - Go to "User Management" > "Users"
   - Select the user you created
   - Go to the "Roles" tab
   - Assign the user to one of the roles (Tool Viewer, Tool Editor, or Tool Admin)

4. **Obtain a token for the user**:
   - You can use the Auth0 Authentication API to obtain a token for this user
   - See Method 3 for details on using the Authentication API

## Method 3: Using Auth0 Authentication API Directly

You can also use the Auth0 Authentication API directly to obtain tokens.

### Prerequisites
- Auth0 domain
- Auth0 client ID and client secret
- API audience

### Steps

1. **Make a request to the Auth0 token endpoint**:
   ```bash
   curl --request POST \
     --url 'https://YOUR_AUTH0_DOMAIN/oauth/token' \
     --header 'content-type: application/json' \
     --data '{
       "client_id":"YOUR_CLIENT_ID",
       "client_secret":"YOUR_CLIENT_SECRET",
       "audience":"YOUR_API_AUDIENCE",
       "grant_type":"client_credentials"
     }'
   ```

   Replace:
   - `YOUR_AUTH0_DOMAIN` with your Auth0 domain (e.g., `udacity-cofshp.us.auth0.com`)
   - `YOUR_CLIENT_ID` with your Auth0 client ID
   - `YOUR_CLIENT_SECRET` with your Auth0 client secret
   - `YOUR_API_AUDIENCE` with your API audience (e.g., `https://securityapp/`)

2. **Extract the token from the response**:
   The response will be a JSON object containing an `access_token` field. This is your JWT token.

## Using Tokens in API Requests

Once you have obtained a token, you can use it to make authenticated requests to the API:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://127.0.0.1:5000/api/tools
```

Replace `YOUR_TOKEN` with the token you obtained.

## Environment Variable Configuration

The API uses several environment variables for authentication configuration. Make sure these are set correctly:

### Required Environment Variables

- **`AUTH0_DOMAIN`**: Your Auth0 domain (e.g., `udacity-cofshp.us.auth0.com`)
- **`API_AUDIENCE`** or **`API_IDENTIFIER`**: The audience value for your API (e.g., `https://securityapp/`)
- **`AUTH0_CLIENT_ID`**: Your Auth0 client ID (for token generation)
- **`AUTH0_CLIENT_SECRET`**: Your Auth0 client secret (for token generation)

### Setting Environment Variables

You can set these variables in several ways:

1. **Using the `.env` file**:
   ```
   AUTH0_DOMAIN='udacity-cofshp.us.auth0.com'
   API_AUDIENCE='https://securityapp/'
   API_IDENTIFIER='https://securityapp/'
   AUTH0_CLIENT_ID='your-client-id'
   AUTH0_CLIENT_SECRET='your-client-secret'
   ```

2. **Using the `setup.sh` script**:
   ```bash
   source setup.sh
   ```

3. **Setting them directly in your terminal**:
   ```bash
   export AUTH0_DOMAIN='udacity-cofshp.us.auth0.com'
   export API_AUDIENCE='https://securityapp/'
   export API_IDENTIFIER='https://securityapp/'
   export AUTH0_CLIENT_ID='your-client-id'
   export AUTH0_CLIENT_SECRET='your-client-secret'
   ```

**Note**: Make sure both `API_AUDIENCE` and `API_IDENTIFIER` are set to the same value to avoid inconsistencies.

## Troubleshooting

### Token is Invalid or Expired

If you receive a 401 Unauthorized error with a message like "Token expired" or "Invalid token", your token may have expired or be malformed. The error message will include additional context to help you diagnose the issue:

- **"Token expired"**: Your token has expired. Obtain a new token using one of the methods above.
- **"Incorrect claims. Please, check the audience and issuer"**: The audience (`aud`) or issuer (`iss`) claim in your token doesn't match what the API expects. Make sure your token was issued for the correct audience (`https://securityapp/`) and by the correct Auth0 tenant.

### Missing Permissions

If you receive a 403 Forbidden error with a message like "Permission not found", your token does not have the required permissions for the endpoint you're trying to access. The error message will include the available permissions in your token, which can help you identify what permissions you have and what you need.

For example, if you try to access an endpoint that requires the `create:tools` permission but your token only has `read:tools`, you'll receive an error message like:
```
Permission "create:tools" not found. Available permissions: read:tools
```

Make sure you're using a token with the appropriate role and permissions for the endpoint you're trying to access.

### Client Authentication Failed

If you receive an error when trying to obtain a token, check that your Auth0 client ID and client secret are correct. Also, make sure that the client is authorized to request tokens for the specified audience.

Common error messages include:
- **"Client authentication failed"**: Your client ID or client secret is incorrect.
- **"Unauthorized client"**: Your client is not authorized to request tokens for the specified audience.
- **"Invalid audience"**: The audience you specified doesn't exist or your client is not authorized to request tokens for it.

### Malformed Token Errors

If you receive a 400 Bad Request error with messages like "Not enough segments" or "Token is malformed or invalid", this indicates that the token you're using doesn't have the correct JWT format. A valid JWT token should have three segments separated by dots (header.payload.signature). Common causes include:

- Copying only part of the token
- Including extra characters or spaces in the token
- Using a token that was generated for a different purpose

Make sure you copy the entire token exactly as provided by the Auth0 API or the `sending_token_API.py` script. Do not add any extra characters, and ensure there are no line breaks or spaces in the token.

### SSL Connection Errors

If you encounter SSL errors when the API tries to validate your token (such as "EOF occurred in violation of protocol"), this could be due to:

- Network connectivity issues
- Firewall or proxy settings blocking the connection
- SSL certificate validation problems

Try running the API on a different network or check your network configuration to ensure it can connect to the Auth0 domain.

### Other Issues

If you encounter other issues, check the Auth0 logs in the Auth0 Dashboard for more information about what might be going wrong.
