import itertools
from typing import List

from django.utils import timezone

from msgs.models import Message

from .models import MailingList
from .tasks import create_messages, send_messages


class MailingListsReport:
    def __init__(self):
        self.mailing_lists = MailingList.objects.all().prefetch_related(
            "messages")
        self.messages = []
        self.extract_messages()

        self.mailing_lists_count = 0
        self.messages_count = 0
        self.message_statuses = {key: 0 for key, value in Message.STATUSES}

        self.count_statistics()

    def count_statistics(self):
        self.mailing_lists_count = self.mailing_lists.count()
        self.messages_count = len(self.messages)

        if self.messages_count != 0:
            for message in self.messages:
                self.message_statuses[message.status] += 1

    def extract_messages(self):
        for mailing_list in self.mailing_lists:
            message_batch = mailing_list.messages.all()
            for message in message_batch:
                self.messages.append(message)


class MailingListReport:
    def __init__(self, pk):
        self.mailing_list = MailingList.objects.prefetch_related(
            "messages__client").get(pk=pk)
        self.messages = self.mailing_list.messages.all()

        self.messages_count = 0
        self.message_statuses = {key: 0 for key, value in Message.STATUSES}

        self.count_statistics()

    def count_statistics(self):
        self.messages_count = len(self.messages)
        for message in self.messages:
            self.message_statuses[message.status] += 1


def mailing_list_create(
    message: str,
    start_at: timezone,
    stop_at: timezone,
    filter_tags: List[str],
    tag_filtering_mode: str
) -> MailingList:

    # Creates a new mailing list
    mailing_list = MailingList(
        message=message,
        start_at=start_at,
        stop_at=stop_at,
        filter_tags=filter_tags,
        tag_filtering_mode=tag_filtering_mode
    )
    mailing_list.save()

    return mailing_list


def force_all_sends():
    create_messages.delay()
    send_messages.delay()


def mailing_list_destroy(pk):
    client = MailingList.objects.get(pk=pk)
    client.delete()


def mailing_list_update(pk, **update_data):
    mailing_list = MailingList.objects.get(pk=pk)

    for key, value in update_data:
        setattr(mailing_list, key, value)

    mailing_list.save()

    return mailing_list


def mailing_lists_statisctics():
    mailing_lists_report = MailingListsReport()

    return mailing_lists_report


def mailing_list_statistics(pk):
    mailing_list_report = MailingListReport(pk)

    return mailing_list_report
