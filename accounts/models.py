from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from backend.models import SoftDeleteManager, SoftDeleteModel
import uuid


class User(SoftDeleteModel, AbstractUser):
   
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    session_token = models.UUIDField(default=uuid.uuid4, editable=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  

    objects = UserManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.email

