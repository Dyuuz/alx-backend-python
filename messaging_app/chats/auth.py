from .serializers import RegisterSerializer, CustomLoginSerializer
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from dj_rest_auth.views import LoginView
from rest_framework import status

from .models import User

class RegisterViewset(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('password')
        password = make_password(password)
        User.objects.create(
                        username=serializer.validated_data.get("username"),
                        first_name=serializer.validated_data.get("first_name"),
                        last_name=serializer.validated_data.get("last_name"),
                        email=serializer.validated_data.get("email"),
                        phone_number=serializer.validated_data.get("phone_number"),
                        password=password)
        return Response("Account created successfully", status=status.HTTP_200_OK)


class CustomLoginView(LoginView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CustomLoginSerializer

    # def dispatch(self, request, *args, **kwargs):
    #     for token in OutstandingToken.objects.filter(user=request.user):
    #         try:
    #             BlacklistedToken.objects.get(token=token)
    #         except BlacklistedToken.DoesNotExist:
    #             BlacklistedToken.objects.create(token=token)
    #     return super().dispatch(request, *args, **kwargs)

    def get_response(self):
        response_data = super().get_response()
        # Removes user data and return only access and refresh token
        response_data.data.pop("user")
        
        return Response(data=response_data.data)