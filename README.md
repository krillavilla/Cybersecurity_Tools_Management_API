# Cybersecurity Tools Management API

Udacity Full Stack Web Development Capstone Project

---

## Motivation for the Project

The **Cybersecurity Tools Management API** is designed to provide a centralized platform for managing various cybersecurity tools. This project aims to streamline the process of integrating and utilizing different tools, making it easier for cybersecurity professionals to manage their workflows efficiently.

---

## URL Location for the Hosted API

The API is hosted at: [https://your-api-url.com](https://your-api-url.com)

---

## Project Dependencies

- Python 3.8+
- Flask
- Flask-JWT-Extended
- Gunicorn
- Requests

---

## Local Development and Hosting Instructions

### Setting Up the Project

1. **Clone the repository:**
   ```bash
   git clone https://github.com/krillavilla/Cybersecurity_Tools_Management_API.git
   cd Cybersecurity_Tools_Management_API
   ```

2. **Create a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Project Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

### Running the Development Server

1. **Set up environment variables:**  
   Create a `.env` file in the root directory and add the following:
   ```env
   AUTH0_DOMAIN=your-auth0-domain
   API_IDENTIFIER=your-api-identifier
   ```

2. **Run the development server:**  
   ```bash
   flask run
   ```

---

## Hosting Instructions

1. Create a `Procfile` in the root directory with the following content:
   ```text
   web: gunicorn app:app
   ```

2. Deploy to your hosting provider (e.g., Heroku, AWS, etc.) following their specific instructions.

---

## Authentication Setup

1. **Set up Auth0:**  
   - Create an Auth0 account and set up a new application.  
   - Configure the API and set the `AUTH0_DOMAIN` and `API_IDENTIFIER` in your `.env` file.

2. **Update the `requires_auth` decorator:**  
   Modify the `requires_auth` function in `app/auth.py` to use your Auth0 credentials.

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

---

## Role-Based Access Control (RBAC)

- **`read:tools`**: Allows reading the list of tools.
- **`create:tools`**: Allows adding new tools.
- **`update:tools`**: Allows updating existing tools.
- **`delete:tools`**: Allows deleting tools.

Ensure that the permissions are correctly set up in your Auth0 dashboard and assigned to the appropriate roles.

---

## Conclusion

This project provides a robust API for managing cybersecurity tools, with secure authentication and role-based access control. Follow the instructions above to set up, develop, and deploy the project.
```

### Changes Made:
1. Adjusted the section hierarchy with consistent `###` and `####` levels.
2. Fixed inconsistent spacing between sections and code blocks.
3. Properly formatted bullet points and subheadings for better readability.
4. Ensured all code blocks are marked with appropriate syntax (e.g., `bash`, `json`, `env`).

