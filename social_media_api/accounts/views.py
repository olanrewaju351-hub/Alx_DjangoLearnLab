# accounts/views.py
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()

class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username", None)
        email = attrs.get("email", None)
        password = attrs.get("password")

        if not password:
            raise serializers.ValidationError({"password": "This field is required."})

        username_field = getattr(User, "USERNAME_FIELD", "username")
        user = None

        # If email provided -> try find user by email then authenticate using username_field
        if email:
            try:
                user_obj = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
            creds = {username_field: getattr(user_obj, username_field), "password": password}
            user = authenticate(**creds)

        # If not found and username provided -> try authenticate using username directly
        if user is None and username:
            creds = {username_field: username, "password": password}
            user = authenticate(**creds)

        # If still none -> fail
        if user is None:
            raise serializers.ValidationError("Unable to log in with provided credentials.")

        if not getattr(user, "is_active", True):
            raise serializers.ValidationError("User account is disabled.")

        attrs["user"] = user
        return attrs


class CustomObtainAuthToken(ObtainAuthToken):
    """
    Accepts either {"username": "...", "password":"..."} OR
    {"email":"...", "password":"..."} and returns token + basic user info.
    """
    serializer_class = CustomAuthTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            "token": token.key,
            "id": getattr(user, "id", None)
        }
        if hasattr(user, "username"):
            data["username"] = user.username
        if hasattr(user, "email"):
            data["email"] = user.email
        return Response(data)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            resp = {
                "id": getattr(user, "id", None),
                "token": token.key,
            }
            if hasattr(user, "email"):
                resp["email"] = getattr(user, "email")
            if hasattr(user, "username"):
                resp["username"] = getattr(user, "username")
            return Response(resp, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  -> returns current user's profile
    PUT  -> replace profile
    PATCH-> partial update (use this for updating just 'bio')
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
