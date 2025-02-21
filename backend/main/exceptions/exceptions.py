from abc import ABC
from http import HTTPStatus
from logging import Logger, getLogger

from django.http import JsonResponse

from main.api.v1.schemas import SMsg
from main.models import Order

logger: Logger = getLogger("django")


class HttpException(Exception, ABC):
    """Базовый класс для исключений."""

    def __init__(self, message: str, status: int) -> None:
        self.status: int = status
        self.response = JsonResponse(
            SMsg(msg=message).model_dump(),
            status=status,
            safe=False,
        )
        logger.warning("HTTP Exception: %s - %s", status, message)
        super().__init__(message)

    def __call__(self) -> JsonResponse:
        return self.response


class Http400EmptyItems(Exception):
    """Исключение для пустого списка блюд."""

    pass


class Http400IncorrectStatus(Exception):
    """Исключение для некорректного статуса заказа."""

    ALLOWED_STATUSES: str = ", ".join(map(str, Order.Status.values))


class Http404ItemsNotFound(Exception):
    """Исключение для несуществующего объекта."""

    pass


class Http404OrderNotFound(Exception):
    """Исключение для несуществующего заказа."""

    pass
