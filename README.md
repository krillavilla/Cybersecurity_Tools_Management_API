
---

# Cybersecurity Tools Management API

The **Cybersecurity Tools Management API** is a centralized platform designed to streamline the organization and utilization of cybersecurity tools. It empowers cybersecurity professionals with efficient workflows and secure access to a wide array of tools.

---

## Hosted API URL

The API is hosted at: [https://securityapp/](https://securityapp/)

---

## Authentication Setup

1. **Set up Auth0**:  
   - Sign up for an Auth0 account and create a new application.  
   - Configure your API settings and add the following in your `.env` file:
     ```env
     AUTH0_DOMAIN=your-auth0-domain
     API_IDENTIFIER=your-api-identifier
     ```
   - Update your Auth0 rules to include the necessary permissions for each endpoint.

2. **Configure the `requires_auth` decorator**:  
   Ensure the `requires_auth` function in `app/auth.py` uses the appropriate Auth0 credentials for token validation and permission checks.

---

## API Documentation

### Endpoints

#### **GET /tools**
- **Description**: Retrieves a list of all available cybersecurity tools.
- **Required Permissions**: `read:tools`
- **Response Example**:
  ```json
  [
    {
      "id": 1,
      "name": "Tool Name",
      "description": "Tool Description"
    }
  ]
  ```

#### **GET /tools/<int:tool_id>**
- **Description**: Retrieves details for a specific tool.
- **Required Permissions**: `read:tools`
- **Response Example**:
  ```json
  {
    "id": 1,
    "name": "Tool Name",
    "description": "Tool Description"
  }
  ```

#### **POST /tools**
- **Description**: Adds a new cybersecurity tool to the database.
- **Required Permissions**: `create:tools`
- **Request Body Example**:
  ```json
  {
    "name": "Tool Name",
    "description": "Tool Description"
  }
  ```
- **Response Example**:
  ```json
  {
    "id": 1,
    "name": "Tool Name",
    "description": "Tool Description"
  }
  ```

#### **PATCH /tools/<int:tool_id>**
- **Description**: Updates an existing tool.
- **Required Permissions**: `update:tools`
- **Request Body Example**:
  ```json
  {
    "name": "Updated Tool Name",
    "description": "Updated Description"
  }
  ```
- **Response Example**:
  ```json
  {
    "id": 1,
    "name": "Updated Tool Name",
    "description": "Updated Description"
  }
  ```

#### **DELETE /tools/<int:tool_id>**
- **Description**: Deletes a tool from the database.
- **Required Permissions**: `delete:tools`
- **Response**: Status code `204` (No Content).

---

## Error Handling

The API returns the following error codes in JSON format:
- **400**: Bad Request  
- **401**: Unauthorized  
- **403**: Forbidden  
- **404**: Not Found  
- **500**: Internal Server Error  

Example error response:
```json
{
  "success": false,
  "error": 404,
  "message": "Not Found"
}
```

---

## Role-Based Access Control (RBAC)

Define and assign the following permissions in the Auth0 dashboard:
- **`read:tools`**: View tools.
- **`create:tools`**: Add new tools.
- **`update:tools`**: Edit existing tools.
- **`delete:tools`**: Remove tools.

---

## Local Development and Hosting Instructions

### Prerequisites
- Python 3.8+
- Flask and Flask-JWT-Extended
- Gunicorn
- Requests library

### Setting Up the Project

1. **Clone the repository**:
   ```bash
   git clone https://github.com/krillavilla/Cybersecurity_Tools_Management_API.git
   cd Cybersecurity_Tools_Management_API
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   AUTH0_DOMAIN=your-auth0-domain
   API_IDENTIFIER=your-api-identifier
   ```

### Running the Development Server

Start the application:
```bash
flask run
```

---

## Testing

Run the test suite using:
```bash
python -m unittest discover -s tests
```

---

## Hosting Instructions

1. **Prepare the application for deployment**:
   - Create a `Procfile` with the following content:
     ```text
     web: gunicorn app:app
     ```

2. **Deploy using a hosting provider**:
   Follow the provider-specific instructions (e.g., Heroku, AWS, etc.) to deploy the app.

---

## Conclusion

The **Cybersecurity Tools Management API** is a robust solution for managing cybersecurity tools. Its secure design, role-based access control, and efficient API endpoints make it an essential tool for cybersecurity professionals. For setup assistance or contributions, refer to the instructions above.

--- 

