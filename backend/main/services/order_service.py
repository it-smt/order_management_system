from decimal import Decimal
from logging import Logger, getLogger

from django.db.models import Q, QuerySet, Sum
from django.shortcuts import get_object_or_404

from main.api.v1.schemas import SItemShow, SOrderAdd, SOrderShow
from main.exceptions.exceptions import (
    Http400IncorrectStatus,
)
from main.models import Item, Order
from main.services.item_service import ItemService

logger: Logger = getLogger("django")


class OrderService:
    """Сервис для работы с заказами."""

    @staticmethod
    def get(
        filter_status: str | None = None, search: str | None = None
    ) -> list[SOrderShow]:
        """
        Получает список заказов с фильтрацией по статусу и поиском.

        Args:
            filter_status (str | None): Статус заказа.
            search (str | None): Поисковый запрос.

        Returns:
            orders (QuerySet[Order]): Список заказов.
        """
        query: Q = Q()

        if filter_status:
            OrderService._validate_status(filter_status)
            query &= Q(status=filter_status)
        if search:
            query &= Q(Q(table_number__icontains=search) | Q(status__icontains=search))

        orders: QuerySet[Order] = Order.objects.filter(query)
        logger.info("Заказов получено: %s", orders.count())

        result: list[SOrderShow] = []
        for order in orders:
            items_ids: list = [item.get("id") for item in order.items]
            items: QuerySet[Item] = ItemService.get(id__in=items_ids)
            for item in items:
                print(item.id, item.name, item.price)
            items_schemas: list[SItemShow] = [
                SItemShow(id=item.id, name=item.name, price=item.price)
                for item in items
            ]

            order_schema: SOrderShow = SOrderShow(
                id=order.id,
                table_number=order.table_number,
                status=order.status,
                items=items_schemas,
                total_price=order.total_price,
            )
            result.append(order_schema)

        return result

    @staticmethod
    def add(data: SOrderAdd) -> Order:
        """
        Создает новый заказ.

        Args:
            data (SOrderAdd): Данные заказа.
        """
        ItemService.check_items(data.items)

        order: Order = Order.objects.create(
            table_number=data.table_number,
            total_price=ItemService.calculate_amount_items(data.items),
            items=[{"id": item.id} for item in data.items],
        )

        logger.info("Заказ #%s успешно создан.", order.id)
        return order

    @staticmethod
    def update(order_id: int, data: SOrderAdd) -> Order:
        """
        Обновляет заказ.

        Args:
            order_id (int): Идентификатор заказа.
            data (SOrderAdd): Данные для обновления заказа.

        Returns:
            JsonResponse: Ответ с данными об обновленном заказе.
        """
        ItemService.check_items(data.items)

        order: Order = get_object_or_404(Order, id=order_id)
        order.table_number = data.table_number
        order.items = [{"id": item.id} for item in data.items]
        order.total_price = ItemService.calculate_amount_items(data.items)
        order.save()

        logger.info(
            "Заказ #%s для столика %s успешно обновлен.", order_id, data.table_number
        )
        return order

    @staticmethod
    def delete(order_id: int) -> None:
        """
        Удаляет заказ по id.

        Args:
            order_id (int): Идентификатор заказа.
        """
        order: Order = get_object_or_404(Order, id=order_id)
        order.delete()
        logger.info("Заказ #%s успешно удален.", order_id)

    @staticmethod
    def change_status(order_id: int, status: str) -> None:
        """
        Изменяет статус заказа.

        Args:
            order_id (int): Идентификатор заказа.
            status (str): Новый статус заказа.
        """
        OrderService._validate_status(status)

        order: Order = get_object_or_404(Order, id=order_id)
        order.status = Order.Status(status).label
        order.save()

        logger.info("Статус заказа #%s успешно изменен на %s.", order_id, status)

    @staticmethod
    def get_statistics() -> dict:
        """Получает статистику по заказам."""
        orders: QuerySet[Order] = Order.objects.all()
        total_revenue: Decimal | None = orders.filter(
            status=Order.Status.PAYED
        ).aggregate(total_revenue=Sum("total_price"))["total_revenue"] or Decimal(0)
        count_waiting: int = orders.filter(status=Order.Status.WAITING).count()
        count_done: int = orders.filter(status=Order.Status.DONE).count()
        count_payed: int = orders.filter(status=Order.Status.PAYED).count()
        logger.info("Статистика по заказам получена.")
        return {
            "total_revenue": total_revenue,
            "count_waiting": count_waiting,
            "count_done": count_done,
            "count_payed": count_payed,
        }

    @staticmethod
    def _validate_status(status: str) -> None:
        """Проверяет корректность статуса заказа."""
        if status in Order.Status.values:
            return True
        logger.warning(
            "Некорректный статус: %s. Ожидались значения: %s",
            status,
            ", ".join(Order.Status.values),
        )
        raise Http400IncorrectStatus
