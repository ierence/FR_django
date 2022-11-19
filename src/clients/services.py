from typing import List

from .models import Client


def client_create(
    phone_number: str,
    service_provider_code: str,
    tags: List[str]
) -> Client:

    client = Client(
        phone_number=phone_number,
        service_provider_code=service_provider_code,
        tags=tags
    )

    client.save()

    return client


def client_update(
    pk: str,
    phone_number: str,
    service_provider_code: str,
    tags: List[str]
) -> Client:

    client = Client.objects.get(pk=pk)

    client.phone_number = phone_number
    client.service_provider_code = service_provider_code
    client.tags = tags

    client.save()

    return client


def client_destroy(pk: str):
    client = Client.objects.get(pk=pk)
    client.delete()
