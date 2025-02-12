from decimal import Decimal
from logging import Logger, getLogger
from typing import Any, Dict, List

from django.db.models import Model, Sum
from django.shortcuts import get_object_or_404

from main.api.v1.schemas import SItem
from main.exceptions import (
    Http400EmptyItems,
    Http400IncorrectStatus,
    Http404ItemsNotFound,
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
    items_ids = [item.id for item in items_ids]
    items: Item = Item.objects.filter(id__in=items_ids).values("id", "price")

    if not items:
        logger.error("Не найдено блюд для идентификаторов %s", items_ids)
        raise Http404ItemsNotFound

    items_dict: dict = {item["id"]: item["price"] for item in items}

    total_amount: Decimal = Decimal(0)

    for item_id in items_ids:
        if item_id not in items_dict:
            logger.warning("Блюдо с id %s не найдено в базе данных.", item_id)
            continue

        total_amount += items_dict[item_id]

    return total_amount


def get_dict_from_item(item_id: int) -> dict:
    """
    Получает словарь из модели Item.

    Args:
        item_id (int): Идентификатор блюда.
    Returns:
        dict: Словарь с полями модели.
    """
    try:
        item: Item = get_object_or_404(Item, id=item_id)
        return {
            "id": item.id,
            "name": item.name,
            "price": item.price,
        }
    except Exception as e:
        logger.error("Ошибка получения блюда с id %s: %s", item_id, str(e))
        raise ValueError(f"Блюдо с id {item_id} не найдено.")


def get_dict_from_model(model: Model) -> Dict:
    """
    Преобразует модель в словарь.

    Args:
        model (Model): Экземпляр модели.

    Returns:
        Dict: Словарь с полями модели.
    """
    model_dict: Dict[str, Any] = {
        field.name: getattr(model, field.name) for field in model._meta.fields
    }

    if isinstance(model, Order):
        if "items" in model_dict:
            model_dict["items"] = [
                get_dict_from_item(item.get("id")) for item in model_dict["items"]
            ]

    model_dict.pop("_state", None)

    return model_dict


def status_is_correct(status: str) -> bool:
    """
    Проверяет корректность статуса заказа.

    Args:
        status (str): Статус заказа.

    Returns:
        bool: True, если статус корректен.
    """
    values: List = Order.Status.values
    if status in values:
        return True
    logger.warning(
        "Некорректный статус: %s. Ожидались значения: %s", status, ", ".join(values)
    )
    raise Http400IncorrectStatus


def calculation_revenue() -> Decimal:
    """
    Возвращает общую сумму заказов.

    Returns:
        Decimal: Общая сумма заказов.
    """
    result: Decimal | None = Order.objects.filter(
        status=Order.Status.PAYED.value
    ).aggregate(total_revenue=Sum("total_price"))

    return Decimal(result["total_revenue"] or 0)


def get_count_orders(status: str) -> int:
    """
    Возвращает количество заказов по статусу.

    Args:
        status (str): Статус заказа.

    Returns:
        int: Количество заказов с указанным статусом.
    """
    if not status_is_correct(status):
        logger.warning(
            "Некорректный статус: %s. Ожидались значения: %s",
            status,
            ", ".join(Order.Status.values),
        )
        raise Http400IncorrectStatus

    return Order.objects.filter(status=status).count()


def check_items(items: List[SItem]) -> None:
    """
    Проверяет наличие блюд в списке.

    Args:
        items (List[SItem]): Список блюд.
    """
    if not items:
        logger.warning("Не удалось создать заказ. Должно быть хотя бы одно блюдо.")
        raise Http400EmptyItems
