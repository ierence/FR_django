from rest_framework import serializers


class UUIDSerializertMixin(serializers.Serializer):
    id = serializers.UUIDField()


class CreateUpdateSerializerMixin(serializers.Serializer):
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
