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


class Http400EmptyItems(HttpException):
    """Исключение для пустого списка блюд."""

    def __init__(self) -> None:
        super().__init__(
            "Заказ должен содержать хотя бы одно блюдо.", HTTPStatus.BAD_REQUEST
        )


class Http400IncorrectStatus(HttpException):
    """Исключение для некорректного статуса заказа."""

    _ALLOWED_STATUSES: str = ", ".join(map(str, Order.Status.values))

    def __init__(self) -> None:
        super().__init__(
            f"Статус может иметь только следующие значения: {self._ALLOWED_STATUSES}",
            HTTPStatus.BAD_REQUEST,
        )


class Http404ItemsNotFound(HttpException):
    """Исключение для несуществующего объекта."""

    def __init__(self) -> None:
        super().__init__(
            "Некоторые блюда не были найдены.",
            HTTPStatus.BAD_REQUEST,
        )


class Http404OrderNotFound(HttpException):
    """Исключение для несуществующего заказа."""

    def __init__(self) -> None:
        super().__init__(
            "Заказ не найден.",
            HTTPStatus.NOT_FOUND,
        )
