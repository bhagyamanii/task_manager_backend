from rest_framework import serializers
from .models import Task
from accounts.models import User


class TaskSerializer(serializers.ModelSerializer):
    assigned_users = serializers.SlugRelatedField(
        slug_field="email",
        queryset=User.objects.all(),
        many=True,
        required=False
    )

    owner = serializers.EmailField(source="owner.email", read_only=True)

    class Meta:
        model = Task
        fields = [
            "task_id", "title", "description",
            "is_completed", "assigned_users",
            "owner",
            "created_at", "updated_at"
        ]
        read_only_fields = ["task_id", "created_at", "updated_at", "owner"]
