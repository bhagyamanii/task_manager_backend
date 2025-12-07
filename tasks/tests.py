from rest_framework.test import APITestCase
from rest_framework import status
import uuid

from accounts.models import User
from tasks.models import Task
from rbac.models import Role, Permission, RolePermission, UserRole


class TaskAPITestCase(APITestCase):

    def setUp(self):

        #user-create admin+normal TEST
        self.admin = User.objects.create_user(
            email="admin@test.com",
            username="admin",
            password="admin123"
        )

        self.user = User.objects.create_user(
            email="user@test.com",
            username="user",
            password="user123"
        )

        #role-create
        self.admin_role = Role.objects.create(name="Admin")
        self.user_role = Role.objects.create(name="User")

        #perms 
        perms = {
            "task.create",
            "task.view",
            "task.update",
            "task.delete",
            "task.admin"
        }

        perm_objs = {}
        for code in perms:
            perm_objs[code] = Permission.objects.create(code=code)

        #allPerms - admin
        for p in perm_objs.values():
            RolePermission.objects.create(role=self.admin_role, permission=p)

        #CRU perms -user
        for code in ["task.create", "task.view", "task.update"]:
            RolePermission.objects.create(role=self.user_role, permission=perm_objs[code])

        #roleAssign
        UserRole.objects.create(user=self.admin, role=self.admin_role)
        UserRole.objects.create(user=self.user, role=self.user_role)

        #tasks
        self.admin_task = Task.objects.create(
            title="Admin Task",
            description="Admin description",
            owner=self.admin
        )

        self.user_task = Task.objects.create(
            title="User Task",
            description="User description",
            owner=self.user
        )

        #logic
        self.admin_token = self.get_token("admin@test.com", "admin123")
        self.user_token = self.get_token("user@test.com", "user123")

    #helper funs
    def get_token(self, email, password):
        res = self.client.post("/api/auth/token/", {
            "email": email,
            "password": password
        })
        return res.data["access"]

    def auth(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    
    #tests = CRUD + RBAC
    def test_create_task(self):
        self.auth(self.user_token)

        res = self.client.post("/api/tasks/task/", {
            "title": "User Created Task",
            "description": "hello"
        })
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


    def test_user_sees_only_own_tasks(self):
        self.auth(self.user_token)

        res = self.client.get("/api/tasks/task/")

        data = res.data.get("results", res.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "User Task")


    def test_admin_sees_all_tasks(self):
        self.auth(self.admin_token)

        res = self.client.get("/api/tasks/task/")
        data = res.data.get("results", res.data)
        self.assertEqual(len(data), 2)


    def test_admin_can_access_any_task(self):
        self.auth(self.admin_token)

        res = self.client.get(f"/api/tasks/{self.user_task.task_id}/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_user_can_update_own_task(self):
        self.auth(self.user_token)

        res = self.client.patch(
            f"/api/tasks/{self.user_task.task_id}/",
            {"title": "Updated"},
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
