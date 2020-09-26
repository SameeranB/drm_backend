from allauth.account.models import EmailAddress
from django.urls import reverse
from rest_framework import status

from users_module.tests.test_setup import TestAuthenticationSetup, TestUserSetup


class TestAuthenticationViews(TestAuthenticationSetup):

    def test_user_registration_success(self):
        res = self.client.post(self.register_url, self.user_registration_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_registration_failure_no_data(self):
        res = self.client.post(self.register_url)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_failure_email_unverified(self):
        self.client.post(self.register_url, self.user_registration_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_success(self):
        res = self.client.post(self.register_url, self.user_registration_data, format="json")
        email = self.user_data['email']
        user = EmailAddress.objects.get(email=email)
        user.verified = True
        user.save()
        res = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class TestUserViews(TestUserSetup):

    def test_user_create_family_medical_history(self):
        response = self.client.post(reverse('user-family-medical-history', args={'user_id': self.user.user_id}),  data=self.user_family_medical_history, format="json")
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        pass

    def test_user_update_family_medical_history(self):
        pass

    def test_user_delete_family_medical_history(self):
        pass

    def test_user_add_medication(self):
        pass

    def test_user_delete_medication(self):
        pass

    def test_user_set_daily_routine(self):
        pass

    def test_user_set_payment_method(self):
        pass

    def test_user_request_payment_confirmation(self):
        pass

    def test_user_set_personal_information(self):
        pass

    def test_user_set_personal_medical_history(self):
        pass

    def test_user_retrieve_user_self(self):
        pass

    def test_user_retrieve_user_others(self):
        pass

    def test_admin_retrieve_user(self):
        pass

    def test_admin_list_users_success(self):
        pass

    def test_admin_list_users_failure(self):
        pass

    def test_admin_confirm_success(self):
        pass

    def test_admin_confirm_failure(self):
        pass
