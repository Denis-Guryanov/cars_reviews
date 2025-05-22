# Car Reviews API

API для управления отзывами об автомобилях. Проект реализован с использованием Django и Django Rest Framework (DRF). 
Поддерживает CRUD-операции для моделей: Страна, Производитель, Автомобиль, Комментарий. 
Экспорт данных в форматы XLSX и CSV. Аутентификация через токен для защищенных операций.

---

## 📋 Требования

- Python
- Django
- PostgreSQL
- Установленные зависимости: `djangorestframework`, `pandas`, `openpyxl`, `psycopg2-binary` (для PostgreSQL).

---

## 🚀 Установка

1. Клонируйте репозиторий:
```
git clone https://github.com/Denis-Guryanov/Car_reviews.git
```
Установите зависимости:
```
poetry install
```
🛠 Настройка базы данных
Создайте БД (PostgreSQL) и настройте подключение в settings.py:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'car_reviews_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Примените миграции:

```
python manage.py migrate
```

🔥 Запуск
```
python manage.py runserver
```

Сервер будет доступен по адресу: http://localhost:8000.

📡 Использование API
Эндпоинты
Модель	URL	Методы
Страны	/reviews/api/countries/	GET, POST, PUT, DELETE
Производители	/reviews/api/manufacturers/	GET, POST, PUT, DELETE
Автомобили	/reviews/api/cars/	GET, POST, PUT, DELETE
Комментарии	/reviews/api/comments/	GET, POST, PUT, DELETE
Экспорт данных
CSV: /reviews/api/<model>/export/?type=csv

XLSX: /reviews/api/<model>/export/?type=xlsx

JSON (по умолчанию): /reviews/api/<model>/export/

Пример:

```
http://localhost:8000/reviews/api/comments/export/?type=xlsx
```

🔐 Авторизация
Требуется токен для операций:

Создание/редактирование/удаление: Страны, Производители, Автомобили.

Редактирование/удаление комментариев.

Публичный доступ:

Просмотр всех данных.

Добавление комментариев.

Получение токена:
Создайте суперпользователя:

```python manage.py createsuperuser```
Получите токен:
```
python manage.py drf_create_token <username>
```