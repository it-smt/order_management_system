from typing import List
from django.db import models


class Item(models.Model):
    """Модель блюда."""

    name = models.CharField(verbose_name="Название", max_length=100)
    price = models.DecimalField(
        verbose_name="Цена", default=0, max_digits=10, decimal_places=2
    )

    class Meta:
        verbose_name: str = "Блюдо"
        verbose_name_plural: str = "Блюда"
        ordering: List[str] = ["-id"]

    def __str__(self) -> str:
        return f"{self.name} - {self.price}"


class Order(models.Model):
    """Модель заказа."""

    class Status(models.TextChoices):
        """Статусы заказа."""

        WAITING = "В ожидании", "В ожидании"
        PAYED = "Оплачено", "Оплачено"
        DONE = "Готово", "Готово"

    table_number = models.PositiveIntegerField(verbose_name="Номер стола")
    items = models.JSONField(verbose_name="Блюда", default=list)
    total_price = models.DecimalField(
        verbose_name="Общая стоимость", default=0, max_digits=10, decimal_places=2
    )
    status = models.CharField(
        verbose_name="Статус",
        max_length=10,
        choices=Status.choices,
        default=Status.WAITING.value,
    )

    class Meta:
        verbose_name: str = "Заказ"
        verbose_name_plural: str = "Заказы"
        ordering: List[str] = ["-id"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Заказ для столика #{self.table_number} - {self.total_price}"
