from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.deprecation import MiddlewareMixin


class SessionJWTMiddleware(MiddlewareMixin):

    def process_request(self, request):
        auth = JWTAuthentication()

        try:
            user_auth = auth.authenticate(request)
        except:
            return None

        if user_auth is None:
            return None

        user, token = user_auth

        jwt_session = token.get("session")

        if jwt_session and str(jwt_session) != str(user.session_token):
            raise AuthenticationFailed("Session expired. Logged in elsewhere.")

        request.user = user
