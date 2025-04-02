# Cybersecurity Tools Management API Reference

This document provides detailed information about the endpoints available in the Cybersecurity Tools Management API, including request parameters, response formats, and example curl commands.

## Table of Contents

1. [Authentication](#authentication)
2. [Base URL](#base-url)
3. [Error Handling](#error-handling)
4. [Endpoints](#endpoints)
   - [GET /](#get-)
   - [GET /api/tools](#get-apitools)
   - [GET /api/tools/:id](#get-apitoolsid)
   - [POST /api/tools](#post-apitools)
   - [PATCH /api/tools/:id](#patch-apitoolsid)
   - [DELETE /api/tools/:id](#delete-apitoolsid)
   - [GET /api/users](#get-apiusers)

## Authentication

The API uses Auth0 for authentication and implements Role-Based Access Control (RBAC). To access protected endpoints, you need to include a valid JWT token in the Authorization header:

```
Authorization: Bearer <your_token>
```

There are three roles with different permissions:

1. **Tool Viewer**: Can only view tools
   - Permissions: `read:tools`

2. **Tool Editor**: Can view and edit tools
   - Permissions: `read:tools`, `update:tools`

3. **Tool Admin**: Has full access to tools
   - Permissions: `read:tools`, `create:tools`, `update:tools`, `delete:tools`

For instructions on obtaining a token, refer to the [Authentication Guide](AUTH_GUIDE.md).

## Base URL

The API is hosted at:

- Local: `http://127.0.0.1:5000`
- Production: `https://cybersecurity-tools-api.onrender.com`

## Error Handling

The API returns standard HTTP status codes to indicate the success or failure of a request. In case of an error, the response will include a JSON object with the following structure:

```json
{
  "success": false,
  "error": 404,
  "message": "Resource Not Found"
}
```

Common error codes:

- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 422: Unprocessable Entity
- 500: Internal Server Error

## Endpoints

### GET /

Returns a welcome message.

#### Permissions Required

None

#### Request

```bash
curl https://cybersecurity-tools-api.onrender.com/
```

#### Response

```json
{
  "message": "Welcome to the Cybersecurity Tools Management API!"
}
```

### GET /api/tools

Returns a list of all tools.

#### Permissions Required

`read:tools`

#### Request

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://cybersecurity-tools-api.onrender.com/api/tools
```

#### Response

```json
{
  "success": true,
  "tools": [
    {
      "id": 1,
      "name": "Nmap",
      "description": "Network scanning tool used to discover hosts and services on a computer network.",
      "created_at": "2025-01-20T03:15:24.257200",
      "user_id": 1
    },
    {
      "id": 2,
      "name": "Wireshark",
      "description": "Network protocol analyzer that lets you capture and interactively browse the traffic running on a computer network.",
      "created_at": "2025-01-20T03:18:43.289580",
      "user_id": 1
    }
  ]
}
```

### GET /api/tools/:id

Returns a specific tool by ID.

#### Permissions Required

`read:tools`

#### Request

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://cybersecurity-tools-api.onrender.com/api/tools/1
```

#### Response

```json
{
  "success": true,
  "tool": {
    "id": 1,
    "name": "Nmap",
    "description": "Network scanning tool used to discover hosts and services on a computer network.",
    "created_at": "2025-01-20T03:15:24.257200",
    "user_id": 1
  }
}
```

#### Error Response (404)

```json
{
  "success": false,
  "error": 404,
  "message": "Resource Not Found"
}
```

### POST /api/tools

Creates a new tool.

#### Permissions Required

`create:tools`

#### Request Parameters

| Parameter    | Type   | Description                                 | Required |
|--------------|--------|---------------------------------------------|----------|
| name         | string | The name of the tool                        | Yes      |
| description  | string | A description of the tool                   | Yes      |
| user_id      | integer| The ID of the user who owns the tool        | Yes      |

#### Request

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"name":"Burp Suite", "description":"An integrated platform for performing security testing of web applications", "user_id":1}' \
  https://cybersecurity-tools-api.onrender.com/api/tools
```

#### Response

```json
{
  "success": true,
  "tool": {
    "id": 3,
    "name": "Burp Suite",
    "description": "An integrated platform for performing security testing of web applications",
    "created_at": "2025-01-21T14:30:15.123456",
    "user_id": 1
  }
}
```

#### Error Response (400)

```json
{
  "success": false,
  "error": 400,
  "message": "Bad Request"
}
```

#### Error Response (422)

```json
{
  "success": false,
  "error": 422,
  "message": "Unprocessable Entity"
}
```

### PATCH /api/tools/:id

Updates an existing tool.

#### Permissions Required

`update:tools`

#### Request Parameters

| Parameter    | Type   | Description                                 | Required |
|--------------|--------|---------------------------------------------|----------|
| name         | string | The updated name of the tool                | No       |
| description  | string | The updated description of the tool         | No       |

#### Request

```bash
curl -X PATCH \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"name":"Updated Burp Suite", "description":"Updated description"}' \
  https://cybersecurity-tools-api.onrender.com/api/tools/3
```

#### Response

```json
{
  "success": true,
  "tool": {
    "id": 3,
    "name": "Updated Burp Suite",
    "description": "Updated description",
    "created_at": "2025-01-21T14:30:15.123456",
    "user_id": 1
  }
}
```

#### Error Response (404)

```json
{
  "success": false,
  "error": 404,
  "message": "Resource Not Found"
}
```

#### Error Response (400)

```json
{
  "success": false,
  "error": 400,
  "message": "Bad Request"
}
```

### DELETE /api/tools/:id

Deletes a tool.

#### Permissions Required

`delete:tools`

#### Request

```bash
curl -X DELETE \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://cybersecurity-tools-api.onrender.com/api/tools/3
```

#### Response

```json
{
  "success": true,
  "deleted": 3
}
```

#### Error Response (404)

```json
{
  "success": false,
  "error": 404,
  "message": "Resource Not Found"
}
```

### GET /api/users

Returns a list of all users.

#### Permissions Required

`read:tools`

#### Request

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" https://cybersecurity-tools-api.onrender.com/api/users
```

#### Response

```json
{
  "success": true,
  "users": [
    {
      "id": 1,
      "username": "admin_user",
      "email": "admin@example.com"
    },
    {
      "id": 2,
      "username": "editor_user",
      "email": "editor@example.com"
    },
    {
      "id": 3,
      "username": "viewer_user",
      "email": "viewer@example.com"
    }
  ]
}
```