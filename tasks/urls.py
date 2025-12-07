from django.urls import path
from .views import TaskCreateAPIView, TaskDetailAPIView

urlpatterns = [
    path("task/", TaskCreateAPIView.as_view(), name="task_create"),
    path("<str:task_id>/", TaskDetailAPIView.as_view(), name="task_detail"),
]
