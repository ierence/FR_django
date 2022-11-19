import operator
from functools import reduce
from typing import List

import requests
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from clients.models import Client
from core.celery import app
from mailings.models import MailingList
from msgs.models import Message


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, create_messages.s())
    sender.add_periodic_task(60.0, send_messages.s())


@app.task(bind=True)
@transaction.atomic
def create_messages(*args, **kwargs):
    # Фильтрация активных рассылок
    mailing_lists = get_active_mailing_lists()

    # Обработка рассылок
    for mailing_list in mailing_lists:
        create_messages_for_mailing_list(mailing_list)


def get_active_mailing_lists():
    curr_time = timezone.now()
    mailing_lists = MailingList.objects.filter(
        start_at__lte=curr_time).filter(stop_at__gte=curr_time)

    return mailing_lists


def create_messages_for_mailing_list(mailing_list: MailingList):
    clients = Client.objects.prefetch_related('messages__mailing_list').exclude(
        messages__mailing_list__id=mailing_list.id).distinct()

    privider_q = Q(service_provider_code__contains=mailing_list.filter_tags)
    # отфильтровать клиентов, которым необходимы сообщения
    if mailing_list.tag_filtering_mode == MailingList.ANY:
        q = Q(tags__contains=mailing_list.filter_tags) | privider_q
    elif mailing_list.tag_filtering_mode == MailingList.ALL:
        q = reduce(operator.and_, (Q(tags__contains=[
                   tag]) for tag in mailing_list.filter_tags)) & privider_q

    clients = clients.filter(q)
    # создать новые сообщения
    create_missing_messages(clients, mailing_list)


def create_missing_messages(clients: List[Client], mailing_list: MailingList):
    # Создать сообщения для клиентов, у которых их нет
    for client in clients:
        message = Message(
            status=Message.SCHEDULED,
            client=client,
            mailing_list=mailing_list
        )
        message.save()


@app.task(bind=True)
@transaction.atomic
def send_messages(*args, **kwargs):
    messages = Message.objects.prefetch_related(
        'mailing_list').prefetch_related('client').exclude(status=Message.EXPIRED)

    # Check expired messages
    curr_time = timezone.now()
    expired_messages = messages.filter(mailing_list__stop_at__lte=curr_time)
    for message in expired_messages:
        message.status = message.EXPIRED
        message.save()

    scheduled_messages = messages.filter(
        status__in=[Message.SCHEDULED, Message.FAILED])

    for message in scheduled_messages:
        send_message_to_external_api(message)


def send_message_to_external_api(message: Message):
    try:
        url, headers, body = contruct_request_params(message)
        response = requests.post(
            url=url, headers=headers, json=body
        )
        process_response(response)

    except AssertionError:
        message.status = message.FAILED
    else:
        message.status = message.SUCCESSFUL
        message.sent_at = timezone.now()

    message.save()


def contruct_request_params(message: Message):
    url = "https://probe.fbrq.cloud/v1/send/" + str(message.numeric_id)
    headers = {'Authorization': f"Bearer {settings.EXTERNAL_API_KEY}"}
    body = {
        "id": message.numeric_id,
        "phone": message.client.phone_number,
        "text": message.mailing_list.message
    }

    return url, headers, body


def process_response(response):
    assert response.status_code == 200
    assert response.json()["code"] == 0
