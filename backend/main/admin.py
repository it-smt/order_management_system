from typing import List
from django.contrib import admin

from .models import Item, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Представление блюда в админке."""

    list_display: List[str] = ["id", "name", "price"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Представление заказа в админке."""

    list_display: List[str] = ["id", "table_number", "total_price", "status"]
    list_filter: List[str] = ["status"]
