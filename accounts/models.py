from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from backend.models import SoftDeleteManager, SoftDeleteModel


class User(SoftDeleteModel, AbstractUser):
   
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  

    objects = UserManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.email

