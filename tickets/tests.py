from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from tickets.models import TheatreHall, Genre, Actor, Play, Performance, Reservation, Ticket

User = get_user_model()


class TheatreAPITestCase(APITestCase):
    def setUp(self):
        # Створюємо тестового користувача
        self.user = User.objects.create_user(
            email='test@test.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Створюємо тестові дані
        self.hall = TheatreHall.objects.create(
            name="Test Hall",
            rows=10,
            seats_in_row=15
        )
        
        self.genre = Genre.objects.create(name="Drama")
        self.actor = Actor.objects.create(
            first_name="John",
            last_name="Doe"
        )
        
        self.play = Play.objects.create(
            title="Test Play",
            description="Test Description"
        )
        self.play.genres.add(self.genre)
        self.play.actors.add(self.actor)
        
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.hall,
            show_time="2025-12-25T18:00:00Z"
        )

    def test_get_halls(self):
        """Тест отримання списку залів"""
        url = reverse('theatrehall-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Hall')

    def test_get_plays(self):
        """Тест отримання списку п'єс"""
        url = reverse('play-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Play')

    def test_get_performances(self):
        """Тест отримання списку вистав"""
        url = reverse('performance-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['play']['title'], 'Test Play')

    def test_get_performance_seats(self):
        """Тест отримання інформації про місця"""
        url = reverse('performance-seats', kwargs={'pk': self.performance.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['performance'], self.performance.pk)
        self.assertEqual(response.data['hall']['rows'], 10)
        self.assertEqual(response.data['hall']['seats_in_row'], 15)
        self.assertEqual(len(response.data['taken']), 0)

    def test_create_reservation_authenticated(self):
        """Тест створення резервації авторизованим користувачем"""
        self.client.force_authenticate(user=self.user)
        url = reverse('reservations-list')
        data = {
            'performance_id': self.performance.pk,
            'seats': [{'row': 1, 'seat': 1}, {'row': 1, 'seat': 2}]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 2)

    def test_create_reservation_unauthenticated(self):
        """Тест створення резервації неавторизованим користувачем"""
        url = reverse('reservations-list')
        data = {
            'performance_id': self.performance.pk,
            'seats': [{'row': 1, 'seat': 1}]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_duplicate_seat_reservation(self):
        """Тест спроби забронювати вже зайняте місце"""
        # Спочатку створюємо резервацію
        self.client.force_authenticate(user=self.user)
        url = reverse('reservations-list')
        data = {
            'performance_id': self.performance.pk,
            'seats': [{'row': 1, 'seat': 1}]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Тепер спробуємо забронювати те саме місце
        data = {
            'performance_id': self.performance.pk,
            'seats': [{'row': 1, 'seat': 1}]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_get_my_reservations(self):
        """Тест отримання резервацій користувача"""
        # Створюємо резервацію
        self.client.force_authenticate(user=self.user)
        url = reverse('reservations-list')
        data = {
            'performance_id': self.performance.pk,
            'seats': [{'row': 1, 'seat': 1}]
        }
        self.client.post(url, data, format='json')
        
        # Отримуємо список резервацій користувача
        url = reverse('reservations-my')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
