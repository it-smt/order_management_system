from logging import Logger, getLogger
from typing import Any, Dict

from django.db.models import Model

from main.exceptions import Http404ItemsNotFound
from main.models import Item, Order
from main.services.item_service import ItemService

logger: Logger = getLogger("django")


def get_dict_from_item(item_id: int) -> dict:
    """
    Получает словарь из модели Item.

    Args:
        item_id (int): Идентификатор блюда.
    Returns:
        dict: Словарь с полями модели.
    """
    try:
        item: Item = ItemService.get_one(item_id=item_id)
        return {
            "id": item.id,
            "name": item.name,
            "price": item.price,
        }
    except Exception as e:
        logger.error("Ошибка получения блюда с id %s: %s", item_id, str(e))
        raise Http404ItemsNotFound


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
            try:
                model_dict["items"] = [
                    get_dict_from_item(item.get("id")) for item in model_dict["items"]
                ]
            except Http404ItemsNotFound as e:
                raise e

    model_dict.pop("_state", None)

    return model_dict
