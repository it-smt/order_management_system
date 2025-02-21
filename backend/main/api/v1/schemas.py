from decimal import Decimal
from enum import Enum
from typing import List

from ninja.schema import Schema
from pydantic import condecimal, Field


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
    price: condecimal(gt=0, max_digits=10, decimal_places=2)


class SItemShow(Schema):
    """Схема показа блюда."""

    id: int
    name: str
    price: float


class OrderStatus(Schema):
    """Схема статуса заказа."""

    status: Status


class SOrderAdd(Schema):
    """Схема добавления заказа."""

    table_number: int
    items: list[SItem] = Field(..., min_items=1)


class SOrder(SOrderAdd):
    """Схема заказа."""

    id: int
    total_price: condecimal(gt=0, max_digits=10, decimal_places=2)
    status: Status


class SOrderShow(Schema):
    """Схема показа заказа."""

    id: int
    table_number: int
    items: list[SItemShow]
    total_price: Decimal
    status: str


class SStatistics(Schema):
    """Схема статистики."""

    total_revenue: condecimal(ge=0, max_digits=10, decimal_places=2)
    count_waiting: int = Field(..., ge=0)
    count_done: int = Field(..., ge=0)
    count_payed: int = Field(..., ge=0)
