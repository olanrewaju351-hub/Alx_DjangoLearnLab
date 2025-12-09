# accounts/migrations/0003_populate_usernames_then_make_unique.py
from django.db import migrations, models
import django.utils.timezone

def populate_usernames(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    # iterate existing users and assign a unique username
    for u in User.objects.all():
        if getattr(u, "username", None):
            continue
        # prefer part of email before @ if available
        base = None
        if getattr(u, "email", None):
            base = str(u.email).split("@")[0]
            base = base or "user"
        else:
            base = "user"
        username = base
        counter = 1
        # ensure uniqueness
        while User.objects.filter(username=username).exists():
            username = f"{base}_{counter}"
            counter += 1
        u.username = username
        u.save()

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_bio'),  # adjust to the previous migration name in your repo
    ]

    operations = [
        # 1) add username field as nullable & NOT unique (safe)
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        # 2) populate unique usernames for existing rows
        migrations.RunPython(populate_usernames, reverse_code=migrations.RunPython.noop),
        # 3) alter field to be non-nullable and unique
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]

