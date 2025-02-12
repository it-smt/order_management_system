from decimal import Decimal
from logging import Logger, getLogger

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from main.api.v1.schemas import SItem, SItemAdd
from main.exceptions import Http400EmptyItems, Http404ItemsNotFound
from main.models import Item

logger: Logger = getLogger("django")


class ItemService:
    """Сервис для работы с блюдами."""

    @staticmethod
    def get(**filters) -> QuerySet[Item]:
        """Получает все блюда."""
        return Item.objects.filter(**filters).only("id", "name", "price")

    @staticmethod
    def get_one(item_id: int) -> Item:
        """Получает блюдо по id."""
        return get_object_or_404(Item, id=item_id)

    @staticmethod
    def add(data: SItemAdd) -> Item:
        """
        Добавляет блюдо.

        Args:
            item (SItemAdd): Структура блюда.
        Returns:
            Item: Блюдо.
        """
        return Item.objects.create(name=data.name, price=data.price)

    @staticmethod
    def check_items(items: list[SItem]) -> None:
        """Проверяет наличие блюд в списке."""
        try:
            if not items:
                logger.warning(
                    "Не удалось создать заказ. Должно быть хотя бы одно блюдо."
                )
                raise Http400EmptyItems
        except Http400EmptyItems as e:
            raise e

    @staticmethod
    def calculate_amount_items(items: list[SItem]) -> Decimal:
        """
        Рассчитывает итоговую стоимость блюд.

        Args:
            items (list[SItem]): Список блюд.
        """
        try:
            items_ids: list[int] = [item.id for item in items]
            items: Item = ItemService.get(id__in=items_ids).values("id", "price")

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
        except Http404ItemsNotFound as e:
            raise e
