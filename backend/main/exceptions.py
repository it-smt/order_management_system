from django.http import JsonResponse
from main.api.v1.schemas import SMsg
from main.models import Order


class HttpException(Exception):
    """Базовый класс для исключений."""

    def __init__(self, message: str, status: int) -> None:
        self.message: str = message
        self.status: int = status
        self.response = JsonResponse(
            SMsg(msg=message).model_dump(),
            status=status,
            safe=False,
        )
        super().__init__(self.message)

    def __call__(self) -> JsonResponse:
        return self.response


class Http400EmptyItems(HttpException):
    """Исключение для пустого списка блюд."""

    def __init__(self) -> None:
        super().__init__("Заказ должен содержать хотя бы одно блюдо.", 400)


class Http400IncorrectStatus(HttpException):
    """Исключение для некорректного статуса заказа."""

    def __init__(self) -> None:
        super().__init__(
            f"Статус может иметь только следующие значения: {', '.join(Order.Status.values)}",
            400,
        )
