from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from tasks.models import Task
from tasks.serializers import TaskSerializer
from rbac.services import user_has_permission


class TaskCreateAPIView(APIView):

    def get_queryset(self, request):
        if user_has_permission(request.user, "task.admin"):
            return Task.objects.filter(is_deleted=False)
        return Task.objects.filter(owner=request.user, is_deleted=False)

    def get(self, request):
        if not user_has_permission(request.user, "task.view"):
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        queryset = self.get_queryset(request)

        #search
        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        #filters
        is_completed = request.query_params.get("is_completed")
        if is_completed in ["true", "false"]:
            queryset = queryset.filter(is_completed=(is_completed == "true"))

        assigned_user = request.query_params.get("assigned_user")
        if assigned_user:
            queryset = queryset.filter(assigned_users__email=assigned_user)

        created_after = request.query_params.get("created_after")
        if created_after:
            queryset = queryset.filter(created_at__gte=created_after)

        created_before = request.query_params.get("created_before")
        if created_before:
            queryset = queryset.filter(created_at__lte=created_before)

        queryset = queryset.order_by("-created_at").distinct()

        #pagination
        page = int(request.query_params.get("page", 1))
        limit = int(request.query_params.get("limit", 10))

        start = (page - 1) * limit
        end = start + limit

        total = queryset.count()
        results = queryset[start:end]

        serializer = TaskSerializer(results, many=True)

        return Response({
            "page": page,
            "limit": limit,
            "total": total,
            "results": serializer.data
        })


    def post(self, request):
        if not user_has_permission(request.user, "task.create"):
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(owner=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)



class TaskDetailAPIView(APIView):

    def get_object(self, request, task_id):
        try:
            if user_has_permission(request.user, "task.admin"):
                return Task.objects.get(task_id=task_id, is_deleted=False)
            return Task.objects.get(task_id=task_id, owner=request.user, is_deleted=False)
        except Task.DoesNotExist:
            return None


    def get(self, request, task_id):
        if not user_has_permission(request.user, "task.view"):
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        task = self.get_object(request, task_id)
        if not task:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response(TaskSerializer(task).data)


    def patch(self, request, task_id):
        if not user_has_permission(request.user, "task.update"):
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        task = self.get_object(request, task_id)
        if not task:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


    def delete(self, request, task_id):
        if not user_has_permission(request.user, "task.delete"):
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        task = self.get_object(request, task_id)
        if not task:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        task.delete()
        return Response({"message": "Task deleted"}, status=status.HTTP_204_NO_CONTENT)
