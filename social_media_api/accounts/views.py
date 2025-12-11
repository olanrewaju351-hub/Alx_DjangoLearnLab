# accounts/views.py
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination

from .serializers import (
    RegisterSerializer,
    UserSerializer,
    MiniUserSerializer,
    PostSerializer,
)
from .models import Post

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
    authentication_classes = []  # allow anonymous registration

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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


class FeedPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


def _get_following_relation(user):
    """
    Return a manager representing the users that `user` follows.
    Handles two model shapes:
    1) user.following (related_name from followers M2M)
    2) user.following field defined directly
    """
    # Preferred: user.following exists
    if hasattr(user, 'following'):
        return user.following

    # If only 'followers' exists but related_name='following' on the other side, try access:
    if hasattr(user, 'followers'):
        # If there is a reverse related name that exposes following, try it:
        if hasattr(user, 'following'):
            return user.following

    # Last resort: nothing provided
    raise AttributeError("User model does not expose 'following' or 'followers' relationships.")


class FeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            follows_qs = _get_following_relation(user).all()
        except AttributeError:
            return Response({'detail': 'Follow relation not configured.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Query posts for those authors
        posts_qs = Post.objects.filter(author__in=follows_qs).order_by('-created_at')
        paginator = FeedPagination()
        page = paginator.paginate_queryset(posts_qs, request)
        serializer = PostSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


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


# Follow / unfollow endpoints -------------------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    """
    Follow the user with id=user_id.
    Requesting user cannot follow themselves.
    Returns MiniUserSerializer of target user.
    """
    me = request.user
    target = get_object_or_404(User, pk=user_id)
    if target == me:
        return Response({'detail': "Cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        following_rel = _get_following_relation(me)
    except AttributeError:
        return Response({'detail': "Follow relation not configured on User model."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    following_rel.add(target)
    return Response(MiniUserSerializer(target).data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Unfollow the user with id=user_id.
    """
    me = request.user
    target = get_object_or_404(User, pk=user_id)
    if target == me:
        return Response({'detail': "Cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        following_rel = _get_following_relation(me)
    except AttributeError:
        return Response({'detail': "Follow relation not configured on User model."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    following_rel.remove(target)
    return Response(MiniUserSerializer(target).data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_following_list(request):
    """
    Return list of users the request.user is following.
    """
    try:
        following_rel = _get_following_relation(request.user)
    except AttributeError:
        return Response({'detail': "Follow relation not configured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    qs = following_rel.all()
    data = MiniUserSerializer(qs, many=True).data
    return Response(data, status=status.HTTP_200_OK)

