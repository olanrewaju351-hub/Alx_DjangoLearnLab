from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.

    Keeps username/email/password/permissions behavior and adds:
    - profile_picture: optional ImageField
    - bio: optional TextField
    - followers: directional many-to-many to other users (who follow this user)
    """
    bio = models.TextField(blank=True, null=True)

    profile_picture = models.ImageField(
        upload_to="profile_pics/%Y/%m/%d/",
        blank=True,
        null=True,
    )

    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",
        blank=True,
        help_text="Users who follow this user",
    )

    def __str__(self):
        return self.email or self.username


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='accounts_posts'  # <-- changed to avoid conflict
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"

