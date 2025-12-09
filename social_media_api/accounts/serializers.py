# accounts/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

def _model_field_names(model):
    """Return concrete field names for the model (no m2m)."""
    return {f.name for f in model._meta.concrete_fields}

USER_FIELDS = _model_field_names(User)


# ensure 'bio' and 'profile_picture' are allowed on serializer fields
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'bio', 'profile_picture')
        extra_kwargs = {
            'bio': {'required': False, 'allow_blank': True},
            'profile_picture': {'required': False}
        }



class RegisterSerializer(serializers.ModelSerializer):
    """
    Safe register serializer:
    - Only includes fields that exist on the User model
    - Requires password and hashes it (uses create_user if available)
    """
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        desired = ('id', 'username', 'email', 'password')
        fields = tuple(sorted(set(desired) & USER_FIELDS))
        extra_kwargs = {'email': {'required': True}} if 'email' in USER_FIELDS else {}

    def validate_email(self, value):
        # if email exists on model and should be unique, this avoids duplicate registrations
        if 'email' in USER_FIELDS:
            qs = User.objects.filter(email__iexact=value)
            if qs.exists():
                raise serializers.ValidationError("user with this email already exists.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # keep only model fields
        allowed = {k: v for k, v in validated_data.items() if k in USER_FIELDS}

        create_user = getattr(User.objects, 'create_user', None)
        if callable(create_user):
            try:
                user = create_user(password=password, **allowed)
                if not getattr(user, 'pk', None):
                    user.save()
                return user
            except TypeError:
                # fallback if create_user signature differs
                pass

        user = User(**allowed)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

