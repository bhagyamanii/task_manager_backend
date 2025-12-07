from django.db import models
from backend.models import SoftDeleteModel
from accounts.models import User


class Role(SoftDeleteModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class UserRole(SoftDeleteModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "role")

    
class Permission(SoftDeleteModel):
    code = models.CharField(max_length=100, unique=True) 
    description = models.TextField(blank=True)

    def __str__(self):
        return self.code


class RolePermission(SoftDeleteModel):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("role", "permission")
