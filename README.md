
---

# Cybersecurity Tools Management API

The **Cybersecurity Tools Management API** is a centralized platform for managing a variety of cybersecurity tools. This API streamlines workflows for cybersecurity professionals by providing an organized and efficient system to integrate and utilize tools effectively.

---

## Hosted API URL

The API is hosted at: [https://securityapp/](https://securityapp/)

---

## Authentication Setup

1. **Set up Auth0**:  
   - Create an Auth0 account and set up a new application.  
   - Configure the API by setting the following in your `.env` file:
     ```env
     AUTH0_DOMAIN=your-auth0-domain
     API_IDENTIFIER=your-api-identifier
     ```

2. **Update the `requires_auth` decorator**:  
   Modify the `requires_auth` function in `app/auth.py` to utilize your Auth0 credentials.

---

## API Documentation

### Endpoints

#### **GET /tools**
- **Description**: Retrieve a list of all cybersecurity tools.
- **Permissions**: `read:tools`
- **Response**:
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
- **Description**: Retrieve details of a specific tool.
- **Permissions**: `read:tools`
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Tool Name",
    "description": "Tool Description"
  }
  ```

#### **POST /tools**
- **Description**: Add a new cybersecurity tool.
- **Permissions**: `create:tools`
- **Request Body**:
  ```json
  {
    "name": "Tool Name",
    "description": "Tool Description"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Tool Name",
    "description": "Tool Description"
  }
  ```

#### **PATCH /tools/<int:tool_id>**
- **Description**: Update an existing tool.
- **Permissions**: `update:tools`
- **Request Body**:
  ```json
  {
    "name": "Updated Tool Name",
    "description": "Updated Description"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "name": "Updated Tool Name",
    "description": "Updated Description"
  }
  ```

#### **DELETE /tools/<int:tool_id>**
- **Description**: Delete a specific tool.
- **Permissions**: `delete:tools`
- **Response**:  
  Status code `204` (No Content) on success.

---

## Error Handling

The API handles the following error codes:
- **400**: Bad Request  
- **401**: Unauthorized  
- **403**: Forbidden  
- **404**: Not Found  

Each error response is returned in JSON format:
```json
{
  "success": false,
  "error": 404,
  "message": "Not Found"
}
```

---

## Role-Based Access Control (RBAC)

- **`read:tools`**: Allows viewing the list of tools.
- **`create:tools`**: Allows adding new tools.
- **`update:tools`**: Allows updating existing tools.
- **`delete:tools`**: Allows deleting tools.

Ensure these permissions are set up correctly in the Auth0 dashboard and assigned to appropriate user roles.

---

## Local Development and Hosting Instructions

### Prerequisites

- Python 3.8+
- Flask
- Flask-JWT-Extended
- Gunicorn
- Requests

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

### Running the Development Server

1. **Set up environment variables**:  
   Create a `.env` file in the root directory with the following content:
   ```env
   AUTH0_DOMAIN=your-auth0-domain
   API_IDENTIFIER=your-api-identifier
   ```

2. **Run the server**:
   ```bash
   flask run
   ```

---

## Testing

To run the test suite:
```bash
python -m unittest discover
```

---

## Hosting Instructions

1. **Create a `Procfile`**:  
   Add the following content to a `Procfile` in the root directory:
   ```text
   web: gunicorn app:app
   ```

2. **Deploy to a hosting provider**:  
   Use your hosting provider’s instructions (e.g., Heroku, AWS) to deploy the application.

---

## Conclusion

The Cybersecurity Tools Management API provides a secure and efficient way to manage various cybersecurity tools. With robust authentication, role-based access control, and a clear API structure, this project serves as a reliable solution for cybersecurity professionals. Follow the instructions above to set up, develop, and deploy the application.

--- 

