from django.db import models

from clients.models import Client
from core.models import BaseModel, NumericIDMixin
from mailings.models import MailingList


class Message(NumericIDMixin, BaseModel):
    SCHEDULED = 'sc'
    FAILED = 'fa'
    SUCCESSFUL = 'su'
    EXPIRED = 'ex'

    STATUSES = (
        (SCHEDULED, "scheduled"),
        (FAILED, "failed"),
        (SUCCESSFUL, "successful"),
        (EXPIRED, "expired")
    )

    status = models.CharField(
        choices=STATUSES, max_length=2, default=SCHEDULED)
    sent_at = models.DateTimeField("Отправлено в.", null=True, default=None)
    mailing_list = models.ForeignKey(
        to=MailingList, related_name="messages", on_delete=models.CASCADE)
    client = models.ForeignKey(
        to=Client, related_name="messages", on_delete=models.CASCADE)
