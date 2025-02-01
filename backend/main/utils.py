from decimal import Decimal
from logging import Logger, getLogger
from typing import Dict, List

from django.db.models import Model
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from main.api.v1.schemas import SItem
from main.exceptions import (
    Http400EmptyItems,
    Http400IncorrectStatus,
)
from main.models import Item, Order

logger: Logger = getLogger("django")


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
    """
    Получает словарь из модели Item.

    Args:
        item_id (int): Идентификатор блюда.
    Returns:
        Dict: Словарь с полями модели.
    """
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


def status_is_correct(status: str) -> bool:
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
    logger.info("Не удалось получить заказы. Введен некорректный статус.")
    raise Http400IncorrectStatus


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


def check_items(items: List[SItem]) -> None:
    """
    Проверяет наличие блюд в списке.

    Args:
        items (List[SItem]): Список блюд.
    """
    if len(items) < 1:
        logger.info("Не удалось создать заказ. Должно быть хотя бы одно блюдо.")
        raise Http400EmptyItems
