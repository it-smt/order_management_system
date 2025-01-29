from decimal import Decimal
from enum import Enum
from typing import List
from ninja.schema import Schema


class Status(Enum):
    """Статусы заказа."""

    WAITING: str = "В ожидании"
    PAYED: str = "Оплачено"
    DONE: str = "Готово"


class SMsg(Schema):
    """Схема сообщения."""

    msg: str


class SItem(Schema):
    """Схема блюда."""

    id: int


class SItemAdd(Schema):
    """Схема добавления блюда."""

    name: str
    price: Decimal


class SItemShow(SItemAdd, SItem):
    """Схема показа блюда."""

    pass


class OrderStatus(Schema):
    """Схема статуса заказа."""

    status: Status


class SOrderAdd(Schema):
    """Схема добавления заказа."""

    table_number: int
    items: List[SItem]


class SOrder(SOrderAdd):
    """Схема заказа."""

    id: int
    total_price: Decimal
    status: Status


class SStatistics(Schema):
    """Схема статистики."""

    total_revenue: Decimal
    count_waiting: int
    count_done: int
    count_payed: int
