from decimal import Decimal
from typing import Dict, List

from django.db.models import Model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from main.api.v1.schemas import SItem
from main.models import Item, Order


def calculate_amount_items(items_ids: List[SItem]) -> int:
    """Считает итоговую сумму блюд."""
    amount: Decimal = Decimal(0)

    for item in items_ids:
        obj: Item = get_object_or_404(Item, id=item.id)
        amount += obj.price

    return amount


def get_dict_from_item(item_id):
    item = get_object_or_404(Item, id=item_id).__dict__
    item.pop("_state")
    return item


def get_dict_from_model(model: Model) -> Dict:
    """Преобразует модель в словарь."""
    model_dict: Dict = model.__dict__
    if isinstance(model, Order):
        model_dict["items"] = [
            get_dict_from_item(item.get("id")) for item in model_dict["items"]
        ]
        model_dict["status"] = Order.Status(model.status).label
    model_dict.pop("_state")
    return model_dict


def status_is_correct(status: str) -> bool | JsonResponse:
    """Проверяет корректность статуса заказа."""
    values: List = Order.Status.values
    if status in values:
        return True
    return JsonResponse(
        {"msg": f"Статус может иметь только следующие значения: {', '.join(values)}"},
        status=400,
        safe=False,
    )


def calculation_revenue() -> Decimal:
    """Возвращает общую сумму заказов."""
    orders: List[Order] = Order.objects.filter(status=Order.Status.PAYED.value)
    total_revenue = Decimal(0)
    for order in orders:
        total_revenue += order.total_price
    return total_revenue


def get_count_orders(status: str) -> int:
    """Возвращает количество заказов по статусу."""
    return Order.objects.filter(status=status).count()
