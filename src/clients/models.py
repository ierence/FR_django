import re

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from timezone_field import TimeZoneField

from core.models import BaseModel


class Client(BaseModel):
    # Можно сделать через библиотеку phonenumber_field, но задание требует определённый формат
    phone_number = models.fields.TextField(
        "Номер телефона", unique=True, max_length=11)
    service_provider_code = models.fields.TextField(
        "Код мобильно оператора", help_text="Используется как тэг", max_length=3)
    tags = ArrayField(
        models.CharField("Тэг", max_length=20),
        default=list
    )
    time_zone = TimeZoneField(verbose_name="Часовой пользователь пользователя")

    class Meta:
        abstract = False

    def clean(self) -> None:
        # Валидация номера телефона
        phone_pattern = re.compile("7[0-9]{10}")
        if phone_pattern.match(self.phone_number) == False:
            raise ValidationError(
                ("Неверный формат номера. Номер должен иметь формат 7XXXXXXXXXX, где X - цифры от 0 до 9.")
            )

        # Валидация кода оператора
        if self.phone_number[1:4] != self.service_provider_code:
            raise ValidationError(
                "Код мобильного оператора не совпадает с указанным в номере телефона."
            )
