import uuid
from random import randint

from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(
        "Создано", db_index=True, default=timezone.now)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        abstract = True


def generate_numeric_id():
    return randint(0, 9223372036854775807)


class NumericIDMixin(models.Model):
    numeric_id = models.BigIntegerField(
        "Цифровой ID", default=generate_numeric_id)

    class Meta:
        abstract = True
