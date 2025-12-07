from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import uuid

class CustomTokenObtainSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        user.session_token = uuid.uuid4()
        user.save(update_fields=["session_token"])

        data["session"] = str(user.session_token)

        return data


class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer
