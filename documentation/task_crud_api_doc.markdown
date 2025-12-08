# Task Manager API – Full Documentation

A complete, secure, role-based **Task Management System** built with Django REST Framework, JWT + Session Protection, Soft Delete, and granular RBAC permissions.

---

## Base URL

```
http://localhost:8000/api/tasks/
```

All endpoints require authentication except login/signup.

---

## Authentication (JWT + Anti-Session Hijacking)

| Endpoint                     | Method | Purpose                            |
|-----------------------------|--------|-------------------------------------|
| `POST /api/auth/token/`     | POST   | Login → Get access + refresh token |
| `POST /api/auth/token/refresh/` | POST   | Refresh access token               |

See full [Authentication Docs here](#authentication--session-protection)

---

## RBAC Permission System

### Permissions Used

| Code               | Description                       |
|--------------------|-----------------------------------|
| `task.view`        | Can list & view tasks             |
| `task.create`      | Can create new tasks              |
| `task.update`      | Can edit tasks                    |
| `task.delete`      | Can delete tasks                  |
| `task.admin`       | Full access (bypass ownership)    |

Admins with `task.admin` can manage **all** tasks.  
Regular users can only manage tasks they **own**.

---

## Task Endpoints

### 1. List & Search Tasks

**Endpoint**: `GET /api/tasks/task/`

**Permissions Required**: `task.view`

#### Request Query Parameters

| Parameter           | Type    | Description                              | Example                     |
|---------------------|---------|------------------------------------------|-----------------------------|
| `search`            | string  | Search in title/description              | `?search=bug`               |
| `is_completed`      | bool    | Filter by completion                     | `?is_completed=true`        |
| `assigned_user`     | string  | Filter by assigned user email            | `?assigned_user=john@co.com`|
| `created_after`     | date    | ISO date (YYYY-MM-DD)                    | `?created_after=2025-01-01` |
| `created_before`    | date    | ISO date                                 | `?created_before=2025-12-31`|
| `page`              | int     | Pagination page                          | `?page=2`                   |
| `limit`             | int     | Items per page (default 10)                  | `?limit=20`                 |

#### Example Request

```http
GET /api/tasks/task/?search=frontend&is_completed=false&page=1&limit=15
Authorization: Bearer <access_token>
```

#### Success Response

```json
{
  "page": 1,
  "limit": 15,
  "total": 42,
  "results": [
    {
      "task_id": "TK1",
      "title": "Fix login bug",
      "description": "Users can't login with Google",
      "is_completed": false,
      "assigned_users": ["alice@company.com", "bob@company.com"],
      "owner": "john@company.com",
      "created_at": "2025-04-05T10:30:00Z",
      "updated_at": "2025-04-06T14:22:11Z"
    }
  ]
}
```

---

### 2. Create Task

**Endpoint**: `POST /api/tasks/task/`

**Permission**: `task.create`

#### Request Body

```json
{
  "title": "Implement dark mode",
  "description": "Add toggle in settings",
  "is_completed": false,
  "assigned_users": ["dev1@company.com", "designer@company.com"]
}
```

#### Success Response (201)

```json
{
  "task_id": "TK42",
  "title": "Implement dark mode",
  "description": "Add toggle in settings",
  "is_completed": false,
  "assigned_users": ["dev1@company.com", "designer@company.com"],
  "owner": "currentuser@company.com",
  "created_at": "2025-04-07T08:15:22Z",
  "updated_at": "2025-04-07T08:15:22Z"
}
```

---

### 3. Retrieve Task Detail

**Endpoint**: `GET /api/tasks/<str:task_id>/`

**Permission**: `task.view`

#### Example

```http
GET /api/tasks/TK42/
```

#### Response

Same format as create, full task object.

---

### 4. Update Task (Partial)

**Endpoint**: `PATCH /api/tasks/<str:task_id>/`

**Permission**: `task.update`

#### Request Body (any fields)

```json
{
  "title": "Implement dark mode v2",
  "is_completed": true,
  "assigned_users": ["newdev@company.com"]
}
```

#### Success (200)

Updated task object

---

### 5. Delete Task (Soft Delete)

**Endpoint**: `DELETE /api/tasks/<str:task_id>/`

**Permission**: `task.delete`

#### Response (204 No Content)

```json
{
  "message": "Task deleted"
}
```

Task is soft-deleted (`is_deleted=True`, `deleted_at` set)

---

## Task Model Details

| Field             | Type           | Description                          |
|-------------------|----------------|--------------------------------------|
| `task_id`         | string         | Auto-generated: `TK1`, `TK2`, ...   |
| `title`           | string         | Required                             |
| `description`     | text           | Optional                             |
| `is_completed`    | boolean        | Default: `false`                     |
| `assigned_users`  | ManyToMany     | Users assigned to task               |
| `owner`           | ForeignKey     | Who created the task (read-only)     |
| `created_at`      | datetime       | Auto-set                             |
| `updated_at`      | datetime       | Auto-updated                         |
| `is_deleted`      | boolean        | Soft delete flag                     |

---

## Permission Flow Example

```mermaid
graph TD
    A[User Requests Task List] --> B{Has task.view?}
    B -->|Yes| C[Has task.admin?]
    C -->|Yes| D[See ALL tasks]
    C -->|No| E[See only OWN tasks]
    B -->|No| F[403 Forbidden]
```

Same logic applies to create/update/delete.

---

## Error Responses

| Status | Response                                    | Cause                              |
|-------|---------------------------------------------|------------------------------------|
| 401   | `{"detail": "Authentication credentials..."}` | Missing/invalid token             |
| 403   | `{"error": "Forbidden"}`                    | Missing required permission        |
| 404   | `{"error": "Task not found"}`               | Invalid `task_id`                  |
| 400   | Validation errors                           | Bad input data                     |

---

## Swagger Documentation

Live interactive docs available at:

```
http://localhost:8000/api/docs/
```

Includes:
- All endpoints
- Request/response examples
- Try-it-out functionality
- Schema download

---

## Summary Table

| Method | Endpoint                     | Permission Required     | Description                     |
|-------|------------------------------|--------------------------|----------------------------------|
| GET   | `/api/tasks/task/`           | `task.view`              | List & filter tasks              |
| POST  | `/api/tasks/task/`           | `task.create`            | Create new task                  |
| GET   | `/api/tasks/TK123/`          | `task.view`              | Get single task                  |
| PATCH | `/api/tasks/TK123/`          | `task.update`            | Update task                      |
| DELETE| `/api/tasks/TK123/`          | `task.delete`            | Soft delete task                 |

---

**This is a production-ready, secure, scalable task management API with proper ownership, permissions, pagination, search, and filtering.**

Perfect for integration into admin panels, team dashboards, or project management tools.

Let your frontend team know:  
All task IDs are like `TK42`  
Ownership matters — non-admins can only edit their own tasks  
Soft delete = tasks disappear but are recoverable  
Use Swagger for testing!