## API Documentation

### Endpoints

#### GET /api/v1/main/orders

##### Возвращает список всех заказов.

##### Parameters

- **filter_status (string | null)**: Статус заказа для фильтрации.
- **search (string | null)**: Строка для поиска по номеру стола или статусу заказа.

##### Response

- **200**: JSON-ответ со списком заказов.

```python
[
	{
		"id": int,
		"table_number": int,
		"items": [
			{
				"id": int
			},
			{
				"id": int
			}
		],
		"total_price": Decimal,
		"status": str
	}
]
```

##### Raises

- **JsonResponse**: Если статус заказа некорректен.

#### POST /api/v1/main/orders

##### Создает новый заказ.

##### Body

```python
{
	"table_number": int, # Номер столика.
	"items": [
		{
			"id": int
		},
		{
			"id": int
		}
	] # Список с id блюд.
}
```

##### Response

- **201**: Ответ с данными о созданном заказе.

```python
{
	"id": int,
	"table_number": int,
	"items": [
		{
			"id": int
		},
		{
			"id": int
		}
	],
	"total_price": Decimal,
	"status": str
}
```

- **400**: Ответ с сообщением об ошибке.

##### Raises

- **JsonResponse**: Если заказ не содержит ни одного блюда.

#### PUT /api/v1/main/orders

##### Обновляет заказ.

##### Parameters

- **order_id (integer)**: Идентификатор заказа, который нужно обновить.

##### Body

```python
{
	"table_number": int, # Номер столика.
	"items": [{"id": int}, {"id": int}] # Список id блюд.
}
```

##### Response

- **200**: Ответ с данными об обновленном заказе.

```python
{
	"id": int,
	"table_number": int,
	"items": [
		{
			"id": int
		},
		{
			"id": int
		}
	],
	"total_price": Decimal,
	"status": str
}
```

##### Raises

- **JsonResponse**: Если заказ не содержит ни одного блюда.

#### DELETE /api/v1/main/orders

##### Удаляет заказ.

##### Parameters

- **order_id (integer)**: Идентификатор заказа, который нужно удалить.

##### Response

- **200**: Ответ с сообщением об успешном удалении заказа.

```python
{"msg": str}
```

#### PUT /api/v1/main/orders/status

##### Изменяет статус заказа.

##### Parameters

- **order_id (integer)**: Идентификатор заказа, для которого нужно изменить статус.
- **status (str)**: Новый статус заказа.

##### Response

- **200**: Ответ с сообщением об успешном изменении статуса заказа.

```python
{"msg": str}
```

##### Raises

- **JsonResponse**: Если переданный статус заказа некорректен.

#### GET /api/v1/main/statistics

##### Возвращает статистику по заказам.

##### Response

- **200**: Ответ со статистикой по заказам.

```python
{
  "total_revenue": Decimal,
  "count_waiting": int,
  "count_done": int,
  "count_payed": int
}
```

#### POST /api/v1/main/items

##### Добавляет новое блюдо.

##### Body

```python
{
	"name": str,
	"price": Decimal
}
```

##### Response

- **201**: Ответ с данными о созданном блюде.

```python
{
  "id": int,
  "name": str,
  "price": Decimal
}
```

#### GET /api/v1/main/items

##### Возвращает список всех блюд.

##### Response

- **200**: Ответ со списком всех блюд.

```python
[
  {
    "id": int,
    "name": str,
    "price": Decimal
  }
]
```
