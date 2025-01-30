from decimal import Decimal
from typing import Dict, List

from django.db.models import Model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from main.api.v1.schemas import SItem
from main.models import Item, Order


def calculate_amount_items(items_ids: List[SItem]) -> Decimal:
    """
    Считает итоговую сумму блюд.

    Args:
        items_ids (List[SItem]): Список идентификаторов блюд.

    Returns:
        Decimal: Итоговая сумма блюд.
    """
    return sum(get_object_or_404(Item, id=item.id).price for item in items_ids)


def get_dict_from_item(item_id: int) -> dict:
    item: Dict = get_object_or_404(Item, id=item_id).__dict__
    item.pop("_state")
    return item


def get_dict_from_model(model: Model) -> Dict:
    """
    Преобразует модель в словарь.

    Args:
        model (Model): Экземпляр модели.

    Returns:
        Dict: Словарь с полями модели.
    """
    model_dict: Dict = model.__dict__
    if isinstance(model, Order):
        model_dict["items"] = [
            get_dict_from_item(item.get("id")) for item in model_dict["items"]
        ]
        model_dict["status"] = Order.Status(model.status).label
    model_dict.pop("_state")
    return model_dict


def status_is_correct(status: str) -> bool | JsonResponse:
    """
    Проверяет корректность статуса заказа.

    Args:
        status (str): Статус заказа.

    Returns:
        bool | JsonResponse: True, если статус корректен, иначе JsonResponse с сообщением об ошибке.
    """
    values: List = Order.Status.values
    if status in values:
        return True
    return JsonResponse(
        {"msg": f"Статус может иметь только следующие значения: {', '.join(values)}"},
        status=400,
        safe=False,
    )


def calculation_revenue() -> Decimal:
    """
    Возвращает общую сумму заказов.

    Returns:
        Decimal: Общая сумма заказов.
    """
    return sum(
        order.total_price
        for order in Order.objects.filter(status=Order.Status.PAYED.value)
    )


def get_count_orders(status: str) -> int:
    """
    Возвращает количество заказов по статусу.

    Args:
        status (str): Статус заказа.

    Returns:
        int: Количество заказов с указанным статусом.
    """
    return Order.objects.filter(status=status).count()
