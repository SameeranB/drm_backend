from django.urls import reverse
from rest_framework.test import APITestCase


class TestAuthenticationSetup(APITestCase):

    def setUp(self):
        self.register_url = reverse('rest_register')
        self.login_url = reverse('rest_login')

        self.user_registration_data = {
            'email': 'email@gmail.com',
            "password1": 'password1234',
            "password2": 'password1234',
            "first_name": "User",
            "last_name": "Test"
        }

        self.user_data = {
            'email': 'email@gmail.com',
            "password": 'password1234',
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class TestUserSetup(APITestCase):

    def setUp(self):
        self.user_data = {
            'email': 'email@gmail.com',
            "password1": 'password1234',
            "password2": 'password1234',
            "first_name": "User",
            "last_name": "Test"
        }

        self.admin_data = {
            'email': 'admin@gmail.com',
            "password1": 'password1234',
            "password2": 'password1234',
            "first_name": "admin",
            "last_name": "Test"
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
