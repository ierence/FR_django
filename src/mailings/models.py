from django.contrib.postgres.fields import ArrayField
from django.db import models

from core.models import BaseModel


class MailingList(BaseModel):
    ALL = 'all'
    ANY = 'any'

    FILTERING_CHOICES = (
        (ALL, 'all'),
        (ANY, 'any')
    )

    message = models.fields.TextField("Текст рассылки")
    start_at = models.fields.DateTimeField()
    stop_at = models.fields.DateTimeField()
    tag_filtering_mode = models.CharField(
        choices=FILTERING_CHOICES, max_length=3)
    filter_tags = ArrayField(
        models.CharField("Тэг", max_length=20)
    )
