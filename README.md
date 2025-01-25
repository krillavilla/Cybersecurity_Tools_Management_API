
# Cybersecurity Tools Management API

The **Cybersecurity Tools Management API** is a centralized platform designed to streamline the organization and utilization of cybersecurity tools. It empowers cybersecurity professionals with efficient workflows and secure access to a wide array of tools.

---

## Motivation

The goal of this project is to create a backend API that manages a centralized repository of cybersecurity tools, including role-based access control for various users (e.g., tool administrators and users). 

This project demonstrates skills in backend development, secure authentication using Auth0, database management, and deploying scalable APIs on platforms like Heroku. It is designed to solve real-world problems in the cybersecurity domain by organizing tools into functional categories and ensuring secure and efficient access for users.

---

## Hosted API URL

The API is hosted live at: **[https://securityapp.herokuapp.com](https://securityapp.herokuapp.com)**  

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
- **Heroku**: For deploying and hosting the API.
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
   Create a `.env` file in the root directory:
   ```env
   FLASK_APP=app.py
   FLASK_ENV=development
   DATABASE_URL=your_postgresql_database_url
   AUTH0_DOMAIN=your-auth0-domain
   API_IDENTIFIER=your-api-identifier
   ```

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

## Hosting Instructions (Heroku)

1. **Install the Heroku CLI**:
   [Heroku CLI Installation Guide](https://devcenter.heroku.com/articles/heroku-cli)

2. **Login to Heroku**:
   ```bash
   heroku login
   ```

3. **Create a New Heroku App**:
   ```bash
   heroku create your-app-name
   ```

4. **Set Environment Variables on Heroku**:
   - Go to your Heroku dashboard.
   - Navigate to **Settings** → **Reveal Config Vars**.
   - Add the following variables:
     - `DATABASE_URL`: Your PostgreSQL database URL.
     - `AUTH0_DOMAIN`: Your Auth0 domain.
     - `API_IDENTIFIER`: Your API identifier.

5. **Deploy to Heroku**:
   ```bash
   git push heroku main
   ```

6. **Access Your API**:
   Your API will be live at `https://your-app-name.herokuapp.com`.

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

Assign these permissions to roles in the Auth0 dashboard as needed.

---

## Conclusion

The **Cybersecurity Tools Management API** is a robust backend solution designed to support cybersecurity professionals in managing and accessing tools securely. With its efficient RBAC implementation and scalable architecture, this project showcases best practices in modern API development.

For further assistance, open an issue on GitHub or reach out via the repository.

--- 

