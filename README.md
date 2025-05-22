# Проект на Django и Django Rest Framework Отзывы об автомобилях

## Требования
- Docker
- Docker Compose
- Python 3.13
- 
## Установка
1. Для запуска проекта скопируйте его с Github:

```
git clone https://github.com/Denis-Guryanov/Car_reviews.git
```
2. Установите зависимости:
```
poetry install
```
3. Для использования нужен токен, используйте команды:
```
python manage.py createsuperuser
python manage.py drf_create_token <username>
```
## О проекте:
1. Реализованы модели:
- Страна
- Производитель
- Автомобиль
- Комментарий
2. Реализован экспорт данных в форматы xlsx или csv в зависимости от передаваемого в запросе GET параметра c использованием декоратора action
```
http://localhost:8000/reviews/api/comments/export/?type=xlsx или csv
```
3. Используются сериализаторы, viewsets 
