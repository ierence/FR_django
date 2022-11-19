from drf_spectacular.openapi import OpenApiResponse
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


from .serializers import (ClientCreateSerializer, ClientOutputSerializer,
                          ClientUpdateSerializer)
from .services import client_create, client_destroy, client_update


class ClientViewSet(GenericViewSet):
    @extend_schema(
        summary="Создает нового клиента с необходимыми данными.",
        request=ClientCreateSerializer,
        responses={201: ClientOutputSerializer}
    )
    def create(self, request):
        self.serializer_class = ClientCreateSerializer
        self.output_serializer_class = ClientOutputSerializer

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        client = client_create(**serializer.validated_data)
        output_serializer = self.output_serializer_class(client)

        return Response(data=output_serializer.data, status=201)

    @extend_schema(
        summary="Обновляет информацию о клиенте.",
        request=ClientUpdateSerializer,
        responses={204: ClientOutputSerializer}
    )
    def update(self, request, id):
        self.serializer_class = ClientUpdateSerializer
        self.output_serializer_class = ClientOutputSerializer

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        client = client_update(id, **serializer.validated_data)
        output_serializer = self.output_serializer_class(client)

        return Response(data=output_serializer.data, status=204)

    @extend_schema(
        summary="Удаляет клиента.",
        request=None,
        responses={204: OpenApiResponse(description="Клиент удален.")}
    )
    def destroy(self, request, id):

        client_destroy(pk=id)

        return Response(data="Клиент удалён.", status=204)
