from django.http import HttpResponse
from ninja import NinjaAPI

from main.api.v1.schemas import SMsg

from .exceptions import (
    Http400EmptyItems,
    Http400IncorrectStatus,
    Http404ItemsNotFound,
    Http404OrderNotFound,
)


def register_exception_handlers(api: NinjaAPI) -> None:
    @api.exception_handler(Http404OrderNotFound)
    def order_not_found(request, exc) -> HttpResponse:
        """Заказ не найден."""

        return api.create_response(
            request,
            SMsg(msg="Заказ не найден").model_dump(),
            status=404,
        )

    @api.exception_handler(Http404ItemsNotFound)
    def items_not_found(request, exc) -> HttpResponse:
        """Блюда не найдены."""

        return api.create_response(
            request,
            SMsg(msg="Блюда не найдены").model_dump(),
            status=404,
        )

    @api.exception_handler(Http400IncorrectStatus)
    def incorrect_status(request, exc) -> HttpResponse:
        """Некорректный статус заказа."""
        return api.create_response(
            request,
            SMsg(
                msg=f"Статус может иметь только следующие значения: {exc.ALLOWED_STATUSES}"
            ).model_dump(),
            status=400,
        )

    @api.exception_handler(Http400EmptyItems)
    def empty_items(request, exc) -> HttpResponse:
        """В заказе нет блюд."""
        return api.create_response(
            request,
            SMsg(msg="Заказ должен содержать хотя бы одно блюдо.").model_dump(),
            status=400,
        )
