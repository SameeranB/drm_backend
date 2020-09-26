from allauth.account.models import EmailAddress
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users_module.models import User


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
            "password": 'password1234',
            "first_name": "User",
            "last_name": "Test"
        }

        self.admin_data = {
            'email': 'admin@gmail.com',
            "password": 'password1234',
            "first_name": "admin",
            "last_name": "Test"
        }

        self.user_family_medical_history = [
            {
                "type": "Obesity",
                "member": "Mother"
            },
            {
                "type": "Blood Pressure",
                "member": "Father"
            },
            {
                "type": "Cancer",
                "member": "Uncle"
            },
        ]

        self.user = User.objects.create_user(
            email= self.user_data.get("email"),
            password=self.user_data.get("password"),
            first_name=self.user_data.get("first_name"),
            last_name=self.user_data.get("last_name"),
        )

        self.token = Token.objects.create(user=self.user)

        self.api_authentication()

        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="token " + self.token.key)
