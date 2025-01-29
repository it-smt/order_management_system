import pytest
import requests

from main.models import Order


@pytest.mark.django_db
def test_get_orders() -> None:
    """Тестирует эндпоинт /api/v1/main/orders."""
    # Создаем тестовые заказы
    Order.objects.create(table_number="1", items=[{"id": 1}], status="Готово")
    Order.objects.create(table_number="2", items=[{"id": 2}, {"id": 2}])

    # Тестируем функцию без фильтров
    response = requests.get("http://localhost:8000/api/v1/main/orders", timeout=100)
    assert response.status_code == 200
    assert len(response.json()) == 2

    # Тестируем функцию с фильтром по статусу
    response = requests.get(
        "http://localhost:8000/api/v1/main/orders?filter_status=Готово", timeout=100
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["status"] == "Готово"

    # Тестируем функцию с фильтром по поиску
    response = requests.get(
        "http://localhost:8000/api/v1/main/orders?search=1", timeout=100
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["table_number"] == 1
