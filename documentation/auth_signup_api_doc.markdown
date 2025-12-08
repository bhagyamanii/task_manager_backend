# Authentication & User Signup API Documentation

## Overview

This system uses **JWT-based authentication** with an **anti-session-hijacking mechanism** using a unique `session_token` per login.

### Key Security Features

- Email is the primary login identifier (not username)
- Each successful login generates a **new UUID session token**
- JWT contains this `session_token`
- Middleware validates that the session in JWT matches the user's current `session_token`
- If user logs in from another device → old sessions are invalidated
- Soft-delete support for users
- OpenAPI/Swagger documentation available

---

## Base URLs

| Environment | URL |
|-----------|-----|
| Development | `http://localhost:8000/` |
| Production | `https://yourdomain.com/` |

---

## Authentication Endpoints

### 1. Login – Obtain JWT Tokens

**Endpoint**: `POST /api/auth/token/`

**Purpose**: Authenticate user and get access + refresh tokens

#### Request Body

```json
{
  "email": "john@example.com",
  "password": "yourStrongPass123"
}
```

#### Success Response (200 OK)

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "session": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8"
}
```

> The `session` field is critical — it prevents session hijacking.

#### How to Use

Store all three tokens:
- `access` → for API calls (in `Authorization: Bearer <token>`)
- `refresh` → to get new access token when expired
- `session` → stored in user's record; invalidated on next login

---

### 2. Refresh Token

**Endpoint**: `POST /api/auth/token/refresh/`

#### Request Body

```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6..."
}
```

#### Success Response

```json
{
  "access": "new-access-token-here...",
  "session": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8"
}
```

> New access token with same session (if still valid)

#### Error Response (401)

```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

Or if session was invalidated (logged in elsewhere):

```json
{
  "detail": "Session expired. Logged in elsewhere.",
  "code": "authentication_failed"
}
```

---

### 3. User Registration (Self-Serve) Signup

**Endpoint**: `POST /api/accounts/signup/`

**Purpose**: Allow users to register themselves (no admin approval needed)

#### Request Body

```json
{
  "email": "newuser@company.com",
  "username": "newuser123",
  "password": "SecurePass2025!",
  "full_name": "John Doe"
}
```

#### Validation Rules

| Field        | Rules                                      |
|-------------|--------------------------------------------|
| `email`     | Must be unique, valid format                 |
| `password`  | Minimum 6 characters                        |
| `username`  | Required (can be same as email part)        |
| `full_name` | Optional                                   |

#### Success Response (201 Created)

```json
{
  "message": "User registered successfully",
  "user_id": "USR1",
  "email": "newuser@company.com"
}
```

> New user is automatically assigned the role "User" via `UserRole`

#### Error Responses

- **400** – Validation error (e.g., email exists):

```json
{
  "email": ["Email already exists"]
}
```

---

## Security Mechanisms Explained

### Session Token Protection (Anti-Hijacking)

```mermaid
sequenceDiagram
    User->>Backend: Login (email + password)
    Backend-->>User: JWT + session=UUIDv4
    Backend->>Database: Update user.session_token = new UUID
    User->>Backend: API call with JWT
    Backend->>Backend: Extract session from JWT
    Backend->>Database: Compare with user.session_token
    alt Session matches
        Backend-->>User: Success
    else Session mismatch
        Backend-->>User: 401 - Session expired
    end
```

Result: If user logs in from another device → all previous sessions become invalid immediately.

---

## Protected Routes

All endpoints under:

```
/api/tasks/
/api/accounts/ (except signup)
/api/auth/token/
```

require:

```http
Authorization: Bearer <access_token>
```

---

## User Model Highlights

| Field            | Description                              |
|------------------|------------------------------------------|
| `user_id`        | Auto-generated: `USR1`, `USR2`, ...      |
| `email`          | Unique, used for login                   |
| `session_token`  | UUID changed on every login               |
| `is_deleted`     | Soft delete flag                          |
| `deleted_at`     | Timestamp when soft-deleted                      |

> Soft-deleted users cannot log in.

---

## API Documentation (Swagger)

Visit in browser:

```
http://localhost:8000/api/docs/
```

Interactive Swagger UI with:
- Try-it-out functionality
- Schema download (`/api/schema/`)
- All endpoints listed

---

## Summary Table

| Method | Endpoint                     | Purpose                            | Auth Required | Notes                              |
|-------|------------------------------|------------------------------------|---------------|------------------------------------|
| POST  | `/api/auth/token/`           | Login → get tokens                 | No            | Returns `session` token            |
| POST  | `/api/auth/token/refresh/`   | Refresh access token                | No            | Validates session                  |
| POST  | `/api/accounts/signup/`      | Register new user                  | No            | Assigns "User" role automatically  |

---