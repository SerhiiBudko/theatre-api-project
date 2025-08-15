#!/usr/bin/env python3
"""
Демонстраційний скрипт для Theatre API
Показує основні можливості API
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

def print_response(title, response):
    """Виводить відповідь API з заголовком"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"Error: {response.text}")

def demo_api():
    """Демонстрація роботи API"""
    print("🎭 Theatre API Demo")
    print("=" * 50)
    
    # 1. Отримання списку залів
    print("\n1. Отримання списку театральних залів")
    response = requests.get(f"{BASE_URL}/halls/")
    print_response("Театральні зали", response)
    
    # 2. Отримання списку жанрів
    print("\n2. Отримання списку жанрів")
    response = requests.get(f"{BASE_URL}/genres/")
    print_response("Жанри", response)
    
    # 3. Отримання списку акторів
    print("\n3. Отримання списку акторів")
    response = requests.get(f"{BASE_URL}/actors/")
    print_response("Актори", response)
    
    # 4. Отримання списку п'єс
    print("\n4. Отримання списку п'єс")
    response = requests.get(f"{BASE_URL}/plays/")
    print_response("П'єси", response)
    
    # 5. Отримання списку вистав
    print("\n5. Отримання списку вистав")
    response = requests.get(f"{BASE_URL}/performances/")
    print_response("Вистави", response)
    
    # 6. Перегляд вільних місць для першої вистави
    print("\n6. Перегляд вільних місць для вистави")
    response = requests.get(f"{BASE_URL}/performances/1/seats/")
    print_response("Вільні місця", response)
    
    # 7. Реєстрація нового користувача
    print("\n7. Реєстрація нового користувача")
    user_data = {
        "email": f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com",
        "password": "demo123456",
        "first_name": "Demo",
        "last_name": "User"
    }
    response = requests.post(f"{BASE_URL}/user/register/", json=user_data)
    print_response("Реєстрація користувача", response)
    
    if response.status_code == 201:
        user_email = user_data["email"]
        
        # 8. Отримання JWT токену
        print("\n8. Отримання JWT токену")
        token_data = {
            "email": user_email,
            "password": "demo123456"
        }
        response = requests.post(f"{BASE_URL}/user/token/", json=token_data)
        print_response("JWT токен", response)
        
        if response.status_code == 200:
            access_token = response.json()["access"]
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # 9. Створення резервації
            print("\n9. Створення резервації")
            reservation_data = {
                "performance_id": 1,
                "seats": [
                    {"row": 5, "seat": 10},
                    {"row": 5, "seat": 11}
                ]
            }
            response = requests.post(f"{BASE_URL}/reservations/", 
                                   json=reservation_data, 
                                   headers=headers)
            print_response("Створення резервації", response)
            
            # 10. Перегляд резервацій користувача
            print("\n10. Перегляд резервацій користувача")
            response = requests.get(f"{BASE_URL}/reservations/my/", headers=headers)
            print_response("Мої резервації", response)
            
            # 11. Перегляд оновлених вільних місць
            print("\n11. Перегляд оновлених вільних місць")
            response = requests.get(f"{BASE_URL}/performances/1/seats/")
            print_response("Оновлені вільні місця", response)
            
            # 12. Спроба забронювати вже зайняте місце
            print("\n12. Спроба забронювати вже зайняте місце")
            duplicate_data = {
                "performance_id": 1,
                "seats": [{"row": 5, "seat": 10}]
            }
            response = requests.post(f"{BASE_URL}/reservations/", 
                                   json=duplicate_data, 
                                   headers=headers)
            print_response("Спроба дублювання місця", response)
    
    print(f"\n{'='*50}")
    print("🎉 Демонстрація завершена!")
    print("📖 Повна документація API: http://localhost:8000/api/docs/")
    print(f"{'='*50}")

if __name__ == "__main__":
    try:
        demo_api()
    except requests.exceptions.ConnectionError:
        print("❌ Помилка: Не вдалося підключитися до сервера.")
        print("Переконайтеся, що сервер запущений: python manage.py runserver")
    except Exception as e:
        print(f"❌ Помилка: {e}") 