from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    target_str = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'actor_username', 'verb', 'read', 'timestamp', 'target_str']

    def get_target_str(self, obj):
        try:
            return str(obj.target)
        except Exception:
            return None

