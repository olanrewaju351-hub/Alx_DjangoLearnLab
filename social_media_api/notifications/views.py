# notifications/views.py (temporary safe version)
import traceback
import logging
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

logger = logging.getLogger(__name__)

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')
        except Exception as exc:
            # Log full traceback to console so you can inspect
            logger.error("Notifications view error: %s", exc)
            traceback.print_exc()
            # Return empty queryset to avoid a 500 crash
            return Notification.objects.none()

    # final safeguard — if serializer/other code raises, return empty list
    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as exc:
            logger.error("Notifications list error: %s", exc)
            traceback.print_exc()
            return Response([], status=200)

