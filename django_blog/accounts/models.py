from django.db import models
from django.contrib.auth.models import User

def user_profile_path(instance, filename):
    # uploaded to MEDIA_ROOT/profile_photos/user_<id>/<filename>
    return f'profile_photos/user_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to=user_profile_path, blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

