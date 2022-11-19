from rest_framework import serializers

from core.serializers import CreateUpdateSerializerMixin, UUIDSerializertMixin


class ClientCreateSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    service_provider_code = serializers.CharField(min_length=3, max_length=3)
    tags = serializers.ListField(
        child=serializers.CharField()
    )


class ClientOutputSerializer(UUIDSerializertMixin, CreateUpdateSerializerMixin):
    phone_number = serializers.CharField()
    service_provider_code = serializers.CharField(min_length=3, max_length=3)
    tags = serializers.ListField(
        child=serializers.CharField()
    )


class ClientUpdateSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    service_provider_code = serializers.CharField(min_length=3, max_length=3)
    tags = serializers.ListField(
        child=serializers.CharField()
    )
