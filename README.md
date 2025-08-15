# Theatre API

DRF API для театру з можливістю бронювання квитків на вистави.

## Опис проекту

Цей проект представляє собою REST API для театру, який дозволяє:
- Переглядати інформацію про театральні зали, жанри, акторів, п'єси та вистави
- Бронювати квитки на вистави
- Переглядати вільні та зайняті місця
- Керувати резерваціями користувачів

## Технології

- Django 4.2.23
- Django REST Framework 3.16.1
- JWT аутентифікація (djangorestframework-simplejwt)
- Swagger документація (drf-spectacular)
- SQLite база даних

## Встановлення та запуск

1. Клонуйте репозиторій:
```bash
git clone <repository-url>
cd theatre-api-project
```

2. Створіть віртуальне середовище та активуйте його:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/Mac
# або
venv\Scripts\activate  # для Windows
```

3. Встановіть залежності:
```bash
pip install -r requirements.txt
```

4. Виконайте міграції:
```bash
python manage.py migrate
```

5. Створіть суперкористувача:
```bash
python manage.py createsuperuser
```

6. Створіть тестові дані:
```bash
python manage.py create_sample_data
```

7. Запустіть сервер:
```bash
python manage.py runserver
```

## API Endpoints

### Аутентифікація
- `POST /api/user/register/` - Реєстрація нового користувача
- `POST /api/user/token/` - Отримання JWT токену
- `POST /api/user/token/refresh/` - Оновлення JWT токену
- `GET /api/user/me/` - Інформація про поточного користувача

### Театральні зали
- `GET /api/halls/` - Список всіх залів
- `POST /api/halls/` - Створення нового залу (тільки для адміністраторів)
- `GET /api/halls/{id}/` - Деталі залу
- `PUT /api/halls/{id}/` - Оновлення залу (тільки для адміністраторів)
- `DELETE /api/halls/{id}/` - Видалення залу (тільки для адміністраторів)

### Жанри
- `GET /api/genres/` - Список всіх жанрів
- `POST /api/genres/` - Створення нового жанру (тільки для адміністраторів)
- `GET /api/genres/{id}/` - Деталі жанру
- `PUT /api/genres/{id}/` - Оновлення жанру (тільки для адміністраторів)
- `DELETE /api/genres/{id}/` - Видалення жанру (тільки для адміністраторів)

### Актори
- `GET /api/actors/` - Список всіх акторів
- `POST /api/actors/` - Створення нового актора (тільки для адміністраторів)
- `GET /api/actors/{id}/` - Деталі актора
- `PUT /api/actors/{id}/` - Оновлення актора (тільки для адміністраторів)
- `DELETE /api/actors/{id}/` - Видалення актора (тільки для адміністраторів)

### П'єси
- `GET /api/plays/` - Список всіх п'єс
- `POST /api/plays/` - Створення нової п'єси (тільки для адміністраторів)
- `GET /api/plays/{id}/` - Деталі п'єси
- `PUT /api/plays/{id}/` - Оновлення п'єси (тільки для адміністраторів)
- `DELETE /api/plays/{id}/` - Видалення п'єси (тільки для адміністраторів)

### Вистави
- `GET /api/performances/` - Список всіх вистав
- `POST /api/performances/` - Створення нової вистави (тільки для адміністраторів)
- `GET /api/performances/{id}/` - Деталі вистави
- `PUT /api/performances/{id}/` - Оновлення вистави (тільки для адміністраторів)
- `DELETE /api/performances/{id}/` - Видалення вистави (тільки для адміністраторів)
- `GET /api/performances/{id}/seats/` - Перегляд вільних та зайнятих місць

### Резервації
- `GET /api/reservations/` - Список резервацій (тільки для авторизованих користувачів)
- `POST /api/reservations/` - Створення нової резервації (тільки для авторизованих користувачів)
- `GET /api/reservations/my/` - Мої резервації (тільки для авторизованих користувачів)

## Документація API

Swagger документація доступна за адресою: http://localhost:8000/api/docs/

## Приклади використання

### Реєстрація користувача
```bash
curl -X POST http://localhost:8000/api/user/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123", "first_name": "John", "last_name": "Doe"}'
```

### Отримання JWT токену
```bash
curl -X POST http://localhost:8000/api/user/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### Перегляд п'єс
```bash
curl http://localhost:8000/api/plays/
```

### Перегляд вільних місць
```bash
curl http://localhost:8000/api/performances/1/seats/
```

### Створення резервації
```bash
curl -X POST http://localhost:8000/api/reservations/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"performance_id": 1, "seats": [{"row": 1, "seat": 1}, {"row": 1, "seat": 2}]}'
```

### Перегляд моїх резервацій
```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:8000/api/reservations/my/
```

## Моделі даних

### TheatreHall
- `name` - Назва залу
- `rows` - Кількість рядів
- `seats_in_row` - Кількість місць у ряді

### Genre
- `name` - Назва жанру

### Actor
- `first_name` - Ім'я актора
- `last_name` - Прізвище актора

### Play
- `title` - Назва п'єси
- `description` - Опис п'єси
- `genres` - Жанри (ManyToMany з Genre)
- `actors` - Актори (ManyToMany з Actor)

### Performance
- `play` - П'єса (ForeignKey до Play)
- `theatre_hall` - Театральний зал (ForeignKey до TheatreHall)
- `show_time` - Час вистави

### Reservation
- `created_at` - Час створення резервації
- `user` - Користувач (ForeignKey до User)

### Ticket
- `row` - Номер ряду
- `seat` - Номер місця
- `performance` - Вистава (ForeignKey до Performance)
- `reservation` - Резервація (ForeignKey до Reservation)

## Особливості

- JWT аутентифікація з токенами доступу та оновлення
- Автоматична валідація місць при бронюванні
- Перевірка на дублювання місць
- Обмеження швидкості запитів (rate limiting)
- Swagger документація API
- Різні рівні доступу для користувачів та адміністраторів

## Тестування

Для тестування API можна використовувати:
- Swagger UI: http://localhost:8000/api/docs/
- curl команди
- Postman або інші API тестувальники 