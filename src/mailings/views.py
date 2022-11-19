from drf_spectacular.openapi import OpenApiResponse
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import (MailingListCreateSerializer,
                          MailingListOutputSerializer,
                          MailingListRecordOutputSerializer,
                          MailingListsRecordOutputSerializer,
                          MailingListUpdateSerializer)
from .services import (force_all_sends, mailing_list_create,
                       mailing_list_destroy, mailing_list_statistics,
                       mailing_list_update, mailing_lists_statisctics)


class MailingListViewSet(GenericViewSet):
    @extend_schema(
        summary="Создаёт новую рассылку.",
        request=MailingListCreateSerializer,
        responses={201: MailingListOutputSerializer}
    )
    def create(self, request):
        self.serializer_class = MailingListCreateSerializer
        self.output_serializer_class = MailingListOutputSerializer

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        mailing_list = mailing_list_create(**serializer.validated_data)
        output_serializer = self.output_serializer_class(mailing_list)

        return Response(data=output_serializer.data, status=201)

    @extend_schema(
        summary="Обновляет данные о рассылке.",
        request=MailingListUpdateSerializer,
        responses={201: MailingListOutputSerializer}
    )
    def update(self, request, id):
        self.serializer_class = MailingListUpdateSerializer
        self.output_serializer_class = MailingListOutputSerializer

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        mailing_list = mailing_list_update(id, **serializer.validated_data)
        output_serializer = self.output_serializer_class(mailing_list)

        return Response(data=output_serializer.data, status=201)

    @extend_schema(
        summary="Удаляет рассылку.",
        request=None,
        responses={204: OpenApiResponse(description="Рассылка удалена.")}
    )
    def destroy(self, request, id):
        mailing_list_destroy(id)

        return Response(data="Рассылка удалёна.", status=204)

    @extend_schema(
        summary="Форсирует создание и отправку сообщений для всех рассылок.",
        responses={200: OpenApiResponse(description="Форсирование успешно.")}
    )
    @action(detail=False, methods=['get'])
    def force_sends_all(self, request):
        force_all_sends()

        return Response('Форсирование успешно.', status=200)


class MailingListStatsViewSet(GenericViewSet):

    @extend_schema(
        summary="Возвращает общую статистику по всем рассылкам.",
        responses={200: MailingListsRecordOutputSerializer}
    )
    def list(self, request):
        self.serializer_class = MailingListsRecordOutputSerializer

        record = mailing_lists_statisctics()
        serializer = self.serializer_class(record)

        return Response(data=serializer.data, status=200)

    @extend_schema(
        summary="Детальная статистика по сообщениям одной рассылки.",
        responses={200: MailingListRecordOutputSerializer}
    )
    def retrieve(self, request, id):
        self.serializer_class = MailingListRecordOutputSerializer

        record = mailing_list_statistics(id)
        serializer = self.serializer_class(record)

        return Response(data=serializer.data, status=200)
