# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    - Keeps username/email/password/permissions behavior.
    - Adds profile_picture, bio and followers relationship.
    """
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pics/%Y/%m/%d/",
        blank=True,
        null=True
    )

    # followers: users who follow this user.
    # using symmetrical=False so "following" and "followers" are directional.
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",
        blank=True
    )

    def __str__(self):
        # prefer email display if available, else username
        return self.email if getattr(self, "email", None) else self.username

