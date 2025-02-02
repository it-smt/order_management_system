from decimal import Decimal
from logging import Logger, getLogger
from typing import List

from django.db import transaction
from django.db.models import Q, Sum
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from ninja import Router

from main.api.v1.schemas import (
    SItemAdd,
    SItemShow,
    SMsg,
    SOrder,
    SOrderAdd,
    SStatistics,
)
from main.exceptions import Http400EmptyItems, Http400IncorrectStatus
from main.models import Item, Order
from main.utils import (
    calculate_amount_items,
    check_items,
    get_dict_from_model,
    status_is_correct,
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
    query: Q = Q()
    if filter_status:
        try:
            status_is_correct(filter_status)
        except Http400IncorrectStatus as e:
            return e()
        query &= Q(status=filter_status)
    if search:
        query &= Q(Q(table_number__icontains=search) | Q(status__icontains=search))
    orders: List[Order] = Order.objects.filter(query)
    logger.info("Заказов получено: %s", orders.count())
    return JsonResponse([get_dict_from_model(order) for order in orders], safe=False)


@router.post("/orders", response={201: SOrder, 400: SMsg})
@transaction.atomic
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
        check_items(data.items)
    except Http400EmptyItems as e:
        return e()
    order: Order = Order.objects.create(
        table_number=data.table_number,
        total_price=calculate_amount_items(data.items),
        items=[{"id": item.id} for item in data.items],
    )
    order.save()
    logger.info(
        "Заказ #%s для столика %s успешно создан.", order.id, order.table_number
    )

    return JsonResponse(get_dict_from_model(order), status=201, safe=False)


@router.put("/orders", response={200: SOrder})
def order_update(request: HttpRequest, order_id: int, data: SOrderAdd) -> JsonResponse:
    """
    Обновляет заказ.

    Args:
        request (HttpRequest): HTTP-запрос.
        order_id (int): Идентификатор заказа, который нужно обновить.
        data (SOrderAdd): Данные для обновления заказа.

    Returns:
        JsonRespons e: Ответ с данными об обновленном заказе.

    Raises:
        JsonRespons e: Если заказ не содержит ни одного блюда.
    """
    try:
        check_items(data.items)
    except Http400EmptyItems as e:
        return e()
    order: Order = get_object_or_404(Order, id=order_id)
    order.table_number = data.table_number
    order.items = [{"id": item.id} for item in data.items]
    order.total_price = calculate_amount_items(data.items)
    order.save()
    logger.info(
        "Заказ #%s для столика %s успешно обновлен.", order.id, order.table_number
    )
    return JsonResponse(get_dict_from_model(order), status=200, safe=False)


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
    order: Order = get_object_or_404(Order, id=order_id)
    order.delete()
    logger.info("Заказ #%s успешно удален.", order_id)
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
        status_is_correct(status)
    except Http400IncorrectStatus as e:
        return e()
    order: Order = get_object_or_404(Order, id=order_id)
    order.status = Order.Status(status).label
    order.save()
    logger.info("Статус заказа #%s успешно изменен на %s.", order_id, order.status)
    return JsonResponse(
        SMsg(
            msg=f"Статус заказа #{order.id} успешно изменен на {order.status}!"
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
    orders: List[Order] = Order.objects.all()
    total_revenue: Decimal | None = orders.filter(status=Order.Status.PAYED).aggregate(
        total_revenue=Sum("total_price")
    )["total_revenue"] or Decimal(0)
    count_waiting: int = orders.filter(status=Order.Status.WAITING).count()
    count_done: int = orders.filter(status=Order.Status.DONE).count()
    count_payed: int = orders.filter(status=Order.Status.PAYED).count()
    logger.info("Статистика по заказам получена.")
    return JsonResponse(
        SStatistics(
            total_revenue=total_revenue,
            count_waiting=count_waiting,
            count_done=count_done,
            count_payed=count_payed,
        ).model_dump(),
        status=200,
        safe=False,
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
    item: Item = Item.objects.create(
        name=data.name,
        price=data.price,
    )
    item.save()
    return JsonResponse(get_dict_from_model(item), status=201, safe=False)


@router.get("/items", response={200: List[SItemShow]})
def get_items(request: HttpRequest) -> JsonResponse:
    """
    Возвращает список всех блюд.

    Args:
        request (HttpRequest): HTTP-запрос.

    Returns:
        JsonResponse: Ответ со списком всех блюд.
    """
    items: List[Item] = Item.objects.all()
    return JsonResponse([get_dict_from_model(item) for item in items], safe=False)
