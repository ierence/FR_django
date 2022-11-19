from rest_framework import serializers

from core.serializers import CreateUpdateSerializerMixin, UUIDSerializertMixin
from msgs.serializers import MessageSerializer

from .models import MailingList


class MailingListCreateSerializer(serializers.Serializer):
    message = serializers.CharField()
    start_at = serializers.DateTimeField()
    stop_at = serializers.DateTimeField()
    tag_filtering_mode = serializers.ChoiceField(
        choices=MailingList.FILTERING_CHOICES)
    filter_tags = serializers.ListField(
        child=serializers.CharField()
    )


class MailingListUpdateSerializer(serializers.Serializer):
    message = serializers.CharField()
    start_at = serializers.DateTimeField()
    stop_at = serializers.DateTimeField()
    tag_filtering_mode = serializers.ChoiceField(
        choices=MailingList.FILTERING_CHOICES)
    filter_tags = serializers.ListField(
        child=serializers.CharField()
    )


class MailingListOutputSerializer(UUIDSerializertMixin, CreateUpdateSerializerMixin):
    message = serializers.CharField()
    start_at = serializers.DateTimeField()
    stop_at = serializers.DateTimeField()
    tag_filtering_mode = serializers.ChoiceField(
        choices=MailingList.FILTERING_CHOICES)
    filter_tags = serializers.ListField(
        child=serializers.CharField()
    )


class MailingListsRecordOutputSerializer(serializers.Serializer):
    mailing_lists_count = serializers.IntegerField()
    messages_count = serializers.IntegerField()
    message_statuses = serializers.DictField(
        child=serializers.IntegerField(), allow_empty=True)


class MailingListRecordOutputSerializer(serializers.Serializer):
    messages_count = serializers.IntegerField()
    messages = MessageSerializer(many=True)
    message_statuses = serializers.DictField(
        child=serializers.IntegerField(), allow_empty=True)
