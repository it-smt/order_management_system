from typing import List
from django.db.models import Q
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
from main.models import Item, Order
from main.utils import (
    calculate_amount_items,
    get_dict_from_model,
    status_is_correct,
)

router = Router()


@router.get("/orders", response={200: List[SOrder]})
def get_orders(
    request: HttpRequest, filter_status: str | None = None, search: str | None = None
) -> JsonResponse:
    """Возвращает список всех заказов."""
    query: Q = Q()
    if filter_status:
        is_correct: bool | JsonResponse = status_is_correct(filter_status)
        if isinstance(is_correct, JsonResponse):
            return is_correct
        query &= Q(status=filter_status)
    if search:
        query &= Q(Q(table_number__icontains=search) | Q(status__icontains=search))
    orders: List[Order] = Order.objects.filter(query)
    return JsonResponse([get_dict_from_model(order) for order in orders], safe=False)


@router.post("/orders", response={201: SOrder})
def order_add(request: HttpRequest, data: SOrderAdd) -> JsonResponse:
    """Создает новый заказ."""
    print(data)
    order: Order = Order.objects.create(
        table_number=data.table_number,
        total_price=calculate_amount_items(data.items),
        items=[],
    )

    for item in data.items:
        order.items.append({"id": item.id})

    order.save()

    return JsonResponse(get_dict_from_model(order), status=201, safe=False)


@router.put("/orders", response={200: SOrder})
def order_update(request: HttpRequest, order_id: int, data: SOrderAdd) -> JsonResponse:
    """Обновляет заказ."""
    order: Order = get_object_or_404(Order, id=order_id)
    order.table_number = data.table_number
    order.items = []
    for item in data.items:
        order.items.append({"id": item.id})
    order.total_price = calculate_amount_items(data.items)
    order.save()
    return JsonResponse(get_dict_from_model(order), status=200, safe=False)


@router.delete("/orders", response={200: SMsg})
def order_delete(request: HttpRequest, order_id: int) -> JsonResponse:
    """Удаляет заказ."""
    order: Order = get_object_or_404(Order, id=order_id)
    order.delete()
    return JsonResponse(
        SMsg(msg=f"Заказ #{order_id} успешно удален!").model_dump(),
        status=200,
        safe=False,
    )


@router.put("/orders/status", response={200: SMsg})
def change_order_status(
    request: HttpRequest, order_id: int, status: str
) -> JsonResponse:
    """Изменяет статус заказа."""
    order: Order = get_object_or_404(Order, id=order_id)
    order.status = Order.Status(status).label
    order.save()
    return JsonResponse(
        SMsg(
            msg=f"Статус заказа #{order.id} успешно изменен на {order.status}!"
        ).model_dump(),
        status=200,
        safe=False,
    )


@router.get("/statistics", response={200: SStatistics})
def get_statistics(request: HttpRequest) -> JsonResponse:
    """Возвращает статистику по заказам."""
    orders = Order.objects.all()
    total_revenue = sum(
        order.total_price for order in orders.filter(status=Order.Status.PAYED)
    )
    count_waiting = orders.filter(status=Order.Status.WAITING).count()
    count_done = orders.filter(status=Order.Status.DONE).count()
    count_payed = orders.filter(status=Order.Status.PAYED).count()
    return JsonResponse(
        {
            "total_revenue": total_revenue,
            "count_waiting": count_waiting,
            "count_done": count_done,
            "count_payed": count_payed,
        },
        status=200,
        safe=False,
    )


@router.post("/items", response={201: SItemShow})
def add_item(request: HttpRequest, data: SItemAdd) -> JsonResponse:
    """Добавляет новое блюдо."""
    item = Item.objects.create(
        name=data.name,
        price=data.price,
    )
    item.save()
    return JsonResponse(get_dict_from_model(item), status=201, safe=False)


@router.get("/items", response={200: List[SItemShow]})
def get_items(request: HttpRequest) -> JsonResponse:
    """Возвращает список всех блюд."""
    items: List[Item] = Item.objects.all()
    return JsonResponse([get_dict_from_model(item) for item in items], safe=False)
