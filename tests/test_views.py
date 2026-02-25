from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from restaurant.models import Menu,Booking
from restaurant.serializers import MenuSerializer
from rest_framework.authtoken.models import Token


class MenuViewTests(APITestCase):

    def setUp(self):
        Menu.objects.create(title="Pizza", price=10, inventory=5)
        Menu.objects.create(title="Pasta", price=12, inventory=3)

    def test_get_all_menu_items(self):
        url = "/restaurant/menu/items/"
        response = self.client.get(url)

        items = Menu.objects.all()
        serializer = MenuSerializer(items, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_menu_item(self):
        url = "/restaurant/menu/items/"
        data = {"title": "Soup", "price": 5, "inventory": 10}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 3)


    def test_get_all(self):
        items = Menu.objects.all()
        serialized_items = MenuSerializer(items, many=True)
        response = self.client.get('/restaurant/menu/items/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serialized_items.data)


class SingleMenuItemTests(APITestCase):

    def setUp(self):
        self.item = Menu.objects.create(title="Burger", price=8, inventory=4)

    def test_get_single_item(self):
        url = f"/restaurant/menu/items/{self.item.id}/"
        response = self.client.get(url)

        serializer = MenuSerializer(self.item)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_item(self):
        url = f"/restaurant/menu/items/{self.item.id}/"
        data = {"title": "Updated Burger", "price": 9, "inventory": 2}

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, "Updated Burger")

    def test_delete_item(self):
        url = f"/restaurant/menu/items/{self.item.id}/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Menu.objects.count(), 0)


class BookingViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test", password="pass123")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        Booking.objects.create(name="John", no_of_guests=2, booking_date="2024-01-01")

    def test_get_bookings(self):
        url = "/restaurant/booking/tables/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_booking(self):
        url = "/restaurant/booking/tables/"
        data = {"name": "Anna", "no_of_guests": 4, "booking_date": "2024-02-01"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)