import http.client
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Auth0 configuration from environment variables
# These are required for secure token generation
required_vars = ['AUTH0_DOMAIN', 'AUTH0_CLIENT_ID', 'AUTH0_CLIENT_SECRET']
missing_vars = [var for var in required_vars if not os.environ.get(var)]

if missing_vars:
    print("Error: Missing required environment variables:")
    for var in missing_vars:
        print(f"  - {var}")
    print("\nPlease set these variables in your .env file or environment before running this script.")
    print("For security reasons, this script will not run with default values.")
    exit(1)

auth0_domain = os.environ.get('AUTH0_DOMAIN')
client_id = os.environ.get('AUTH0_CLIENT_ID')
client_secret = os.environ.get('AUTH0_CLIENT_SECRET')

# API audience is required for token validation
# Check both API_AUDIENCE and API_IDENTIFIER for backward compatibility
audience = os.environ.get('API_AUDIENCE') or os.environ.get('API_IDENTIFIER')
if not audience:
    print("Error: Missing API_AUDIENCE or API_IDENTIFIER environment variable.")
    print("One of these is required for token generation.")
    exit(1)

# Create the connection to Auth0
conn = http.client.HTTPSConnection(auth0_domain)

# Prepare the payload with the Auth0 credentials
payload_data = {
    "client_id": client_id,
    "client_secret": client_secret,
    "audience": audience,
    "grant_type": "client_credentials"
}

# Convert the payload to JSON
payload = json.dumps(payload_data)

# Set the headers for the request
headers = {'content-type': "application/json"}

# Make the request to Auth0
print(f"Requesting token from {auth0_domain}...")
conn.request("POST", "/oauth/token", payload, headers)

# Get the response
res = conn.getresponse()
data = res.read()

# Parse and print the response
response = json.loads(data.decode("utf-8"))
if 'access_token' in response:
    print("\nToken obtained successfully!")
    print("\nYou can use this token for API requests with the following header:")
    print(f"Authorization: Bearer {response['access_token']}")
    print("\nFull response:")
else:
    print("\nFailed to obtain token. Response:")

print(json.dumps(response, indent=2))
