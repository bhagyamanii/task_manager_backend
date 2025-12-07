from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse
from login.views import CustomTokenObtainView


def home(request):
    return JsonResponse({
        "status": "success",
        "message": "Welcome to the Task Manager"
    })

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    # path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/auth/token/", CustomTokenObtainView.as_view()),
]
