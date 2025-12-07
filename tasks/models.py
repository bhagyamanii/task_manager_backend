from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    task_id = models.CharField(max_length=30, unique=True, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    assigned_users = models.ManyToManyField(
        User,
        related_name="tasks",
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.task_id:
            last_task = Task.objects.all().order_by('id').last()
            next_id = 1 if not last_task else last_task.id + 1
            self.task_id = f"TK{next_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
