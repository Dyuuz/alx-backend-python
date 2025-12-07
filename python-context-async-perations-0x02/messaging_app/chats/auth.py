from .serializers import RegisterSerializer, CustomLoginSerializer
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from dj_rest_auth.views import LoginView
from rest_framework import status

from .models import User

class RegisterViewset(APIView):
    """
    API endpoint to register a new user.

    This view handles POST requests containing user registration data.
    It validates the incoming data using RegisterSerializer, hashes the password,
    and creates a new User object in the database.

    Error Handling:
    - Returns a structured error response if the data is invalid.
    
    Success Response:
    - Returns a JSON object with status, code, and a success message upon account creation.
    
    Authentication & Permissions:
    - This endpoint does not require authentication or permissions.
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        # Handle serializer errors explicitly
        if not serializer.is_valid():
            return Response(
                {
                    "status": "error",
                    "code": "INVALID_DATA",
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # If data is valid, create the user
        password = make_password(serializer.validated_data.get('password'))
        User.objects.create(
            username=serializer.validated_data.get("username"),
            first_name=serializer.validated_data.get("first_name"),
            last_name=serializer.validated_data.get("last_name"),
            email=serializer.validated_data.get("email"),
            phone_number=serializer.validated_data.get("phone_number"),
            password=password
        )

        return Response(
            {
                "status": "success",
                "code": "ACCOUNT_CREATED",
                "message": "Account created successfully"
            },
            status=status.HTTP_201_CREATED
        )


class CustomLoginView(LoginView):
    """
    Custom login view that returns only access and refresh tokens
    after successful authentication.

    Optional:
    - Blacklists all outstanding tokens for the user upon login
      (code is currently commented out).
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = CustomLoginSerializer

    # Optional token blacklisting
    # def dispatch(self, request, *args, **kwargs):
    #     for token in OutstandingToken.objects.filter(user=request.user):
    #         BlacklistedToken.objects.get_or_create(token=token)
    #     return super().dispatch(request, *args, **kwargs)

    def get_response(self):
        """
        Override the default get_response to remove user info
        and return only the access and refresh tokens.
        """
        response_data = super().get_response()
        response_data.data.pop("user", None)  # Safely remove "user" key
        return Response(data=response_data.data)