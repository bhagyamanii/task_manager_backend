from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from accounts.serializers import SignupSerializer
from rbac.models import Role, UserRole


class SignupAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        role = Role.objects.get(name="User")
        UserRole.objects.create(user=user, role=role)

        return Response({
            "message": "User registered successfully",
            "user_id": user.user_id,
            "email": user.email
        }, status=status.HTTP_201_CREATED)
