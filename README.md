
# Cybersecurity Tools Management API

The **Cybersecurity Tools Management API** is a centralized platform designed to streamline the organization and utilization of cybersecurity tools. It empowers cybersecurity professionals with efficient workflows and secure access to a wide array of tools.

---

## Motivation

The goal of this project is to create a backend API that manages a centralized repository of cybersecurity tools, including role-based access control for various users (e.g., tool administrators and users). 

This project demonstrates skills in backend development, secure authentication using Auth0, database management, and deploying scalable APIs on platforms like Render. It is designed to solve real-world problems in the cybersecurity domain by organizing tools into functional categories and ensuring secure and efficient access for users.

---

## Hosted API URL

The API is hosted live at: **[https://cybersecurity-tools-api.onrender.com](https://cybersecurity-tools-api.onrender.com)**  

---

## Project Description

The Cybersecurity Tools Management API allows users to:
- Manage a centralized repository of cybersecurity tools.
- Perform CRUD (Create, Read, Update, Delete) operations on tools.
- Secure the API using role-based access control (RBAC).
- Access tools based on user roles and permissions.

Roles in this project include:
1. **Tool Viewer**: Can view tools.
2. **Tool Editor**: Can view and edit tools.
3. **Tool Admin**: Has full access to the tools (create, read, update, delete).

---

## Dependencies

This project uses the following major dependencies:
- **Flask**: For building the web API.
- **SQLAlchemy**: For database interactions.
- **Flask-Migrate**: To manage database migrations.
- **Auth0**: For secure user authentication and role-based access control.
- **Gunicorn**: A Python WSGI HTTP server for running the application in production.
- **Render**: For deploying and hosting the API.
- **Unittest**: For testing the application.

For the full list of dependencies, refer to `requirements.txt`.

---

## Local Development and Setup

### Prerequisites
- Python 3.8 or later
- Virtual Environment (recommended)
- Flask CLI installed
- PostgreSQL database running locally or remotely

### Steps to Run Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/krillavilla/Cybersecurity_Tools_Management_API.git
   cd Cybersecurity_Tools_Management_API
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Project Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   - Copy the `.env.example` file to `.env`: `cp .env.example .env`
   - Update the `.env` file with your actual values for database URL, Auth0 domain, API identifier, and other sensitive information
   - Alternatively, you can use the `setup.sh` script (see instructions below)
   - Note: Both `.env` and `setup.sh` contain sensitive information and should not be committed to the repository

5. **Run Database Migrations**:
   ```bash
   flask db upgrade
   ```

6. **Start the Development Server**:
   ```bash
   flask run
   ```
   The API will be available at `http://127.0.0.1:5000`.

---

## Hosting Instructions (Render)

1. **Create a Render Account**:
   Sign up for a free account at [Render](https://render.com/).

2. **Connect Your GitHub Repository**:
   - In the Render dashboard, click on "New" and select "Blueprint".
   - Connect your GitHub account and select your repository.

3. **Configure Your Blueprint**:
   - Render will automatically detect the `render.yaml` file in your repository.
   - Review the configuration and click "Apply".

4. **Set Environment Variables**:
   - After the services are created, go to the web service dashboard.
   - Navigate to **Environment** → **Environment Variables**.
   - Add the following variables:
     - `AUTH0_DOMAIN`: Your Auth0 domain.
     - `API_AUDIENCE`: Your API audience.
     - `API_IDENTIFIER`: Your API identifier.
     - `AUTH0_CLIENT_ID`: Your Auth0 client ID.
     - `AUTH0_CLIENT_SECRET`: Your Auth0 client secret.

5. **Deploy Your API**:
   - Render will automatically deploy your API when you push changes to your repository.
   - You can also manually deploy from the Render dashboard.

6. **Access Your API**:
   Your API will be live at `https://cybersecurity-tools-api.onrender.com` (or your custom domain).

---

## API Documentation

### Endpoints

#### **GET /tools**
- **Description**: Retrieve a list of all tools.
- **Required Permissions**: `read:tools`

#### **POST /tools**
- **Description**: Add a new tool.
- **Required Permissions**: `create:tools`

#### **PATCH /tools/<tool_id>**
- **Description**: Update an existing tool.
- **Required Permissions**: `update:tools`

#### **DELETE /tools/<tool_id>**
- **Description**: Delete a tool.
- **Required Permissions**: `delete:tools`

For detailed request/response examples, refer to the `API_REFERENCE.md` file in the repository.

---

## Security Measures

The Cybersecurity Tools Management API implements comprehensive security measures to protect sensitive information while maintaining application functionality:

- **Environment Variable Management**: All sensitive information (API keys, secrets, credentials) is loaded from environment variables with strict validation.
- **No Default Secrets**: The application requires proper environment variables to be set and will not run with insecure defaults.
- **Secure Authentication**: JWT tokens are thoroughly validated for format, signature, expiration, and permissions.
- **Role-Based Access Control**: All endpoints are protected based on user roles and required permissions.
- **Secure Error Handling**: Error responses provide useful information without exposing sensitive details.
- **Secure Testing**: Test files use clearly marked mock tokens and isolated test environments.
- **Version Control Security**: The `.gitignore` file is configured to exclude sensitive files from version control.

### Handling Sensitive Information

To ensure your sensitive information remains secure:

1. **Use Example Files**: The repository includes `.env.example` and `setup.sh.example` files with placeholder values. Copy these to `.env` and `setup.sh` respectively and update with your actual values.
2. **Never Commit Secrets**: Files containing sensitive information (`.env`, `setup.sh`) are excluded in `.gitignore` and should never be committed to version control.
3. **Rotate Compromised Secrets**: If you accidentally commit sensitive information, consider it compromised and rotate those credentials immediately.
4. **Use Environment-Specific Values**: Use different credentials for development, testing, and production environments.
5. **Limit Access**: Restrict access to production credentials to only those who absolutely need them.

For detailed information about security measures and best practices, refer to the [Security Guide](SECURITY.md).

---

## Testing the API

To run the test suite:
```bash
python -m unittest discover -s tests
```

---

## Error Handling

The API provides standard error responses in the following format:
```json
{
  "success": false,
  "error": 404,
  "message": "Resource Not Found"
}
```

---

## Role-Based Access Control (RBAC)

### Permissions
- **`read:tools`**: View tools.
- **`create:tools`**: Add tools.
- **`update:tools`**: Edit tools.
- **`delete:tools`**: Remove tools.

### Roles
- **Tool Viewer**: Can view tools.
  - Permissions: `read:tools`
- **Tool Editor**: Can view and edit tools.
  - Permissions: `read:tools`, `update:tools`
- **Tool Admin**: Has full access to tools.
  - Permissions: `read:tools`, `create:tools`, `update:tools`, `delete:tools`

### Setting Up Authentication

1. **Configure Auth0**:
   - Create an account on [Auth0](https://auth0.com/)
   - Create a new API in your Auth0 dashboard
   - Set the Identifier to `https://securityapp/`
   - Enable RBAC and Add Permissions in the Access Token

2. **Set Up Roles and Permissions**:
   - Create the roles listed above in your Auth0 dashboard
   - Assign the appropriate permissions to each role

3. **Update Environment Variables**:
   - Copy the `setup.sh.example` file to `setup.sh`: `cp setup.sh.example setup.sh`
   - Update the `setup.sh` file with your Auth0 domain, API audience, client ID, and other sensitive information
   - Run `source setup.sh` to set the environment variables
   - Note: `setup.sh` contains sensitive information and should not be committed to the repository

4. **Obtain a Token**:
   - You can use the provided `sending_token_API.py` script to obtain a token
   - Alternatively, you can use the Auth0 Management API or the Auth0 Dashboard to create test users and assign them to roles
   - Use the Auth0 Authentication API to obtain a token for a user with the appropriate role

For detailed instructions on obtaining tokens, refer to the [Authentication Guide](AUTH_GUIDE.md).

For testing purposes, you can use the provided mock tokens in the test files.

---

## Conclusion

The **Cybersecurity Tools Management API** is a robust backend solution designed to support cybersecurity professionals in managing and accessing tools securely. With its efficient RBAC implementation and scalable architecture, this project showcases best practices in modern API development.

For further assistance, open an issue on GitHub or reach out via the repository.

--- 
