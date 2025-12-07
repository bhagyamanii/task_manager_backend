from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from backend.models import SoftDeleteManager, SoftDeleteModel
import uuid


class User(SoftDeleteModel, AbstractUser):
   
    user_id = models.CharField(max_length=30, unique=True, editable=False, null=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    session_token = models.UUIDField(default=uuid.uuid4, editable=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  

    objects = UserManager()
    all_objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.user_id:
            last = User.all_objects.order_by("id").last()
            next_id = 1 if not last else last.id + 1
            self.user_id = f"USR{next_id}"
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.email

