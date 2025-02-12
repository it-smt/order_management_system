from decimal import Decimal
from logging import Logger, getLogger

from django.db.models import Q, QuerySet, Sum
from django.shortcuts import get_object_or_404

from main.api.v1.schemas import SOrderAdd
from main.exceptions import (
    Http400IncorrectStatus,
    Http404OrderNotFound,
)
from main.models import Order
from main.services.item_service import ItemService

logger: Logger = getLogger("django")


class OrderService:
    """Сервис для работы с заказами."""

    @staticmethod
    def get(
        filter_status: str | None = None, search: str | None = None
    ) -> QuerySet[Order]:
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

        orders: QuerySet[Order] = Order.objects.filter(query).only(
            "id", "table_number", "items", "total_price", "status"
        )
        logger.info("Заказов получено: %s", orders.count())
        return orders

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
        order.save()

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

        order: Order = Order.objects.filter(id=order_id)
        if not order.exists():
            raise Http404OrderNotFound
        order.update(
            table_number=data.table_number,
            items=[{"id": item.id} for item in data.items],
            total_price=ItemService.calculate_amount_items(data.items),
        )

        logger.info(
            "Заказ #%s для столика %s успешно обновлен.", order_id, data.table_number
        )

        return order.first()

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

        try:
            Order.objects.get(id=order_id).update(status=Order.Status(status).label)
        except Order.DoesNotExist:
            logger.warning("Заказ с id %s не найден.", order_id)
            raise Http404OrderNotFound

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
        try:
            values: list = Order.Status.values
            if status in values:
                return True
            logger.warning(
                "Некорректный статус: %s. Ожидались значения: %s",
                status,
                ", ".join(values),
            )
            raise Http400IncorrectStatus
        except Http400IncorrectStatus as e:
            raise e
