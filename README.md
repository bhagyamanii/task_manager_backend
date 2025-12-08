# 🚀 task_manager_backend

A robust and scalable backend solution for managing tasks efficiently.

![Version](https://img.shields.io/badge/version-1.0.0-blue)


## ✨ Features

*   🔐 **Secure User Authentication & Authorization:** Manage user accounts and ensure secure access with robust login mechanisms.
*   🛡️ **Role-Based Access Control (RBAC):** Define and assign roles to users, granting granular permissions for different actions and resources.
*   📝 **Comprehensive Task Management:** Create, update, delete, and view tasks with various attributes, designed for efficient organization.
*   ⚡ **High-Performance RESTful API:** Provides a clean and efficient API for seamless integration with frontend applications.
*   🐍 **Scalable Python Architecture:** Built with Python, ensuring maintainability and future scalability for growing demands.

## ⚙️ Installation Guide

Follow these steps to get your `task_manager_backend` up and running on your local machine.

### Prerequisites

Ensure you have the following installed:

*   Python 3.8+
*   pip (Python package installer)

### Step-by-Step Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/bhagyamanii/task_manager_backend.git
    cd task_manager_backend
    ```

2.  **Create a Virtual Environment:**
    It's recommended to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    *   **On macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    *   **On Windows:**
        ```bash
        venv\Scripts\activate
        ```

4.  **Install Dependencies:**
    Install all required packages using pip.
    ```bash
    pip install -r requirements.txt
    ```

5.  **Environment Configuration:**
    Create a `.env` file in the `backend` directory (or root if specified by project structure) for sensitive configurations.
    ```
    # Example .env content
    SECRET_KEY='your_super_secret_key_here'
    DEBUG=True
    DATABASE_URL='sqlite:///db.sqlite3' # Or your PostgreSQL/MySQL connection string
    ```
    *Note: For production, ensure `DEBUG=False` and use a strong `SECRET_KEY`.*

6.  **Apply Database Migrations:**
    Set up your database by applying the necessary migrations.
    ```bash
    python manage.py migrate
    ```

7.  **Create a Superuser (Optional but Recommended):**
    This allows you to access the Django admin panel.
    ```bash
    python manage.py createsuperuser
    ```

8.  **Run the Development Server:**
    Start the backend server.
    ```bash
    python manage.py runserver
    ```
    The backend will typically be accessible at `http://127.0.0.1:8000/`.

## 🚀 Usage Examples

Once the server is running, you can interact with the API using tools like `curl`, Postman, or any HTTP client.

### Basic API Interaction

#### 1. User Login (Example)

To obtain an authentication token:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password"}' http://127.0.0.1:8000/api/login/
```
*Expected Response (example):*
```json
{
    "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0"
}
```

#### 2. Create a Task (Example)

Use the obtained token for authenticated requests:

```bash
curl -X POST -H "Content-Type: application/json" -H "Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0" -d '{"title": "Implement new feature", "description": "Add user profile editing functionality", "status": "pending", "priority": "high"}' http://127.0.0.1:8000/api/tasks/
```
*Expected Response (example):*
```json
{
    "id": 1,
    "title": "Implement new feature",
    "description": "Add user profile editing functionality",
    "status": "pending",
    "priority": "high",
    "assigned_to": null,
    "created_at": "2023-10-27T10:00:00Z",
    "updated_at": "2023-10-27T10:00:00Z"
}
```

#### 3. List All Tasks (Example)

```bash
curl -X GET -H "Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0" http://127.0.0.1:8000/api/tasks/
```

### API Documentation

For a complete list of endpoints, request/response schemas, and authentication details, refer to the API documentation (Swagger)
```bash
http://127.0.0.1:8000/api/docs/
```

### Postman API Endpoints:
```bash
https://.postman.co/workspace/My-Workspace~29597e5a-fce9-4530-87f1-904c810fe56c/collection/41927214-a9f2c7f0-444c-4fe6-a339-a2d9d81be30a?action=share&creator=41927214
```

### Postman Workspace invite link: as there are endpoints saved with defined body structure (if swagger fails):
```bash
https://app.getpostman.com/join-team?invite_code=cc68ab9acc008e078494789d7b1f9af35c0b5cc215674979d43cb21120d4e16a
```


For any inquiries regarding licensing or permissions, please contact the main contributor.

---

**Main Contributor:** bhagyamanii