# Тестовое задание

## Инструкция по запуску

1. Убедитесь, что у вас установлен Docker Compose и запущен Docker Engine
2. Создайте файл **_.env-non-dev_** в корне проекта и поместите в него следующий код:

```
SECRET_KEY=django-insecure-=lw(s=yp3wx%i^su=&ltax!zr4!!w42!^r5(y9d%0#95+t!m1+
DEBUG=True

DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

3. Запустите Docker Compose, выполнив следующую команду в терминале:
   `docker-compose up --build`
4. Дождитесь завершения процесса запуска.

**Важно**: Не сообщайте данные из файла **_.env-non-dev_** другим пользователям, так как они содержат конфиденциальную информацию.

## API Documentation

### Endpoints

**Все эндпоинты можно посмотреть в документации по адресу http://localhost:8000/api/v1/docs**
**Важно**: Проверьте, что запущенные Docker контейнеры работают корректно, иначе ссылка приведет в никуда (Проверить контейнеры можно командой в терминале `docker ps` или же в приложении Docker Desktop)

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
