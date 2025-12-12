# Generated example — prefer `makemigrations` instead of manual file
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('notifications', '0001_initial'),  # adjust to your last migration
        ('contenttypes', '0002_remove_content_type_name'),  # usually safe
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='target_content_type',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='notification',
            name='target_object_id',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]

