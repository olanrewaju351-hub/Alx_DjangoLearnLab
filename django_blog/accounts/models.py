# accounts/models.py
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
    """
    Simple profile stored alongside the built-in User model.
    Extend this with whatever fields you need (bio, photo, etc).
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"


# Signal to automatically create/update Profile when User is saved
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # ensure profile exists for existing users (safe)
        Profile.objects.get_or_create(user=instance)

