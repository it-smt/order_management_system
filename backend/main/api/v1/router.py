from logging import Logger, getLogger
from typing import List

from django.http import HttpRequest, JsonResponse
from ninja import Router

from main.api.v1.schemas import (
    SItemAdd,
    SItemShow,
    SMsg,
    SOrder,
    SOrderAdd,
    SStatistics,
)
from main.exceptions import (
    Http400EmptyItems,
    Http400IncorrectStatus,
    Http404ItemsNotFound,
)
from main.models import Order
from main.services.item_service import ItemService
from main.services.order_service import OrderService
from main.utils import (
    get_dict_from_model,
)

router: Router = Router()

logger: Logger = getLogger("django")


@router.get("/orders", response={200: List[SOrder]})
def get_orders(
    request: HttpRequest, filter_status: str | None = None, search: str | None = None
) -> JsonResponse:
    """
    Возвращает список всех заказов.

    Args:
        request (HttpRequest): HTTP-запрос.
        filter_status (str | None): Статус заказа для фильтрации.
        search (str | None): Строка для поиска по номеру стола или статусу заказа.

    Returns:
        JsonResponse: JSON-ответ со списком заказов.

    Raises:
        JsonResponse: Если статус заказа некорректен.
    """
    try:
        orders: Order = OrderService.get(filter_status, search)
        return JsonResponse(
            [get_dict_from_model(order) for order in orders], safe=False
        )
    except Http400IncorrectStatus as e:
        return e()


@router.post("/orders", response={201: SOrder, 400: SMsg})
def order_add(request: HttpRequest, data: SOrderAdd) -> JsonResponse:
    """
    Создает новый заказ.

    Args:
        request (HttpRequest): HTTP-запрос.
        data (SOrderAdd): Данные для создания заказа.

    Returns:
        JsonResponse: Ответ с данными о созданном заказе или сообщением об ошибке.

    Raises:
        JsonResponse: Если заказ не содержит ни одного блюда.
    """
    try:
        order: Order = OrderService.add(data)
        return JsonResponse(get_dict_from_model(order), status=201, safe=False)
    except (Http400EmptyItems, Http404ItemsNotFound) as e:
        return e()


@router.put("/orders", response={200: SOrder})
def order_update(request: HttpRequest, order_id: int, data: SOrderAdd) -> JsonResponse:
    """
    Обновляет заказ.

    Args:
        request (HttpRequest): HTTP-запрос.
        order_id (int): Идентификатор заказа, который нужно обновить.
        data (SOrderAdd): Данные для обновления заказа.

    Returns:
        JsonResponse: Ответ с данными об обновленном заказе.

    Raises:
        JsonResponse: Если заказ не содержит ни одного блюда.
    """
    try:
        order: Order = OrderService.update(order_id, data)
        return JsonResponse(get_dict_from_model(order), status=200, safe=False)
    except (Http400EmptyItems, Http404ItemsNotFound) as e:
        return e()


@router.delete("/orders", response={200: SMsg})
def order_delete(request: HttpRequest, order_id: int) -> JsonResponse:
    """
    Удаляет заказ.

    Args:
        request (HttpRequest): HTTP-запрос.
        order_id (int): Идентификатор заказа, который нужно удалить.

    Returns:
        JsonResponse: Ответ с сообщением об успешном удалении заказа.
    """
    OrderService.delete(order_id)

    return JsonResponse(
        SMsg(msg=f"Заказ #{order_id} успешно удален!").model_dump(),
        status=200,
        safe=False,
    )


@router.put("/orders/status", response={200: SMsg})
def change_order_status(
    request: HttpRequest, order_id: int, status: str
) -> JsonResponse:
    """
    Изменяет статус заказа.

    Args:
        request (HttpRequest): HTTP-запрос.
        order_id (int): Идентификатор заказа, для которого нужно изменить статус.
        status (str): Новый статус заказа.

    Returns:
        JsonResponse: Ответ с сообщением об успешном изменении статуса заказа.

    Raises:
        JsonResponse: Если переданный статус заказа некорректен.
    """
    try:
        OrderService.change_status(order_id, status)
    except Http400IncorrectStatus as e:
        return e()

    return JsonResponse(
        SMsg(
            msg=f"Статус заказа #{order_id} успешно изменен на {status}!"
        ).model_dump(),
        status=200,
        safe=False,
    )


@router.get("/statistics", response={200: SStatistics})
def get_statistics(request: HttpRequest) -> JsonResponse:
    """
    Возвращает статистику по заказам.

    Args:
        request (HttpRequest): HTTP-запрос.

    Returns:
        JsonResponse: Ответ со статистикой по заказам.
    """
    statistics: dict = OrderService.get_statistics()
    return JsonResponse(
        SStatistics(**statistics).model_dump(),
        status=200,
        safe=False,
    )


@router.get("/items", response={200: List[SItemShow]})
def get_items(request: HttpRequest) -> JsonResponse:
    """
    Возвращает список всех блюд.

    Args:
        request (HttpRequest): HTTP-запрос.

    Returns:
        JsonResponse: Ответ со списком всех блюд.
    """
    return JsonResponse(
        [get_dict_from_model(item) for item in ItemService.get()], safe=False
    )


@router.post("/items", response={201: SItemShow})
def add_item(request: HttpRequest, data: SItemAdd) -> JsonResponse:
    """
    Добавляет новое блюдо.

    Args:
        request (HttpRequest): HTTP-запрос.
        data (SItemAdd): Данные для создания нового блюда.

    Returns:
        JsonResponse: Ответ с данными о созданном блюде.
    """
    return JsonResponse(
        get_dict_from_model(ItemService.add(data)), status=201, safe=False
    )
