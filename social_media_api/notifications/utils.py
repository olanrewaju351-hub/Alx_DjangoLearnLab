from .models import Notification
from django.contrib.contenttypes.models import ContentType

def create_notification(actor, recipient, verb, target=None):
    target_ct = ContentType.objects.get_for_model(target) if target else None
    target_id = target.id if target else None

    Notification.objects.create(
        actor=actor,
        recipient=recipient,
        verb=verb,
        target_ct=target_ct,
        target_id=target_id
    )

