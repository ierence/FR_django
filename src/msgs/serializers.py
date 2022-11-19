from rest_framework import serializers

from core.serializers import CreateUpdateSerializerMixin, UUIDSerializertMixin


class MessageSerializer(UUIDSerializertMixin, CreateUpdateSerializerMixin, serializers.Serializer):
    status = serializers.CharField()
    client = serializers.PrimaryKeyRelatedField(read_only=True)
    sent_at = serializers.DateTimeField()
    mailing_list = serializers.PrimaryKeyRelatedField(read_only=True)
