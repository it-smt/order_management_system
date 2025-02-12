from main.models import Item
from main.api.v1.schemas import SItemAdd


class ItemService:
    """Сервис для работы с блюдами."""

    @staticmethod
    def get() -> list[Item]:
        """Получает все блюда."""
        return Item.objects.all()

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
