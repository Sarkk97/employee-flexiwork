from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase


class EmployeeAuthentication(APITestCase):
    def setUp(self):
        data = {
            'email': "rahman.s@e360africa.com",
            'first_name': 'Rahman',
            'last_name': 'Solanke',
            'staff_no': 'EMP-001',
            'description': 'A good software engineer'
        }
        get_user_model().objects.create_user(**data)

    def test_obtain_token_valid_employee(self):
        url = reverse('token-obtain-pair')
        data = {
            'email': 'rahman.s@e360africa.com',
            'password': 'password'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'access')
        self.assertContains(response, 'refresh')

class EmployeeResetPassword(APITestCase):

    def setUp(self):
        data_1 = {
            'email': "rahman.s@e360africa.com",
            'first_name': 'Rahman',
            'last_name': 'Solanke',
            'staff_no': 'EMP-001',
            'description': 'A good software engineer'
        }
        data_2 = {
            'email': "ahmed.o@e360africa.com",
            'first_name': 'Ahmed',
            'last_name': 'Ojo',
            'staff_no': 'EMP-002',
            'description': 'A good software engineer'
        }
        get_user_model().objects.create_user(**data_1)
        get_user_model().objects.create_user(**data_2)

        ahmed = get_user_model().objects.get(pk=2)
        ahmed.is_active = False
        ahmed.save()

    def test_employee_can_request_for_password_change(self):
        url = reverse('password-reset')
        response = self.client.post(url, {'email': 'rahman.s@e360africa.com'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_inactive_employee_can_not_request_for_password_change(self):
        url = reverse('password-reset')
        response = self.client.post(url, {'email': 'ahmed.o@e360africa.com'}, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_password_reset_link(self):
        url = reverse('password-reset')
        response = self.client.post(url, {'email': 'rahman.s@e360africa.com'}, format='json')

        reset_link = response.json()
        reset_response = self.client.get(reset_link)
        self.assertEqual(reset_response.status_code, status.HTTP_200_OK)
        self.assertEqual(reset_response.json(), 'Valid verification link')

    def test_invalid_token_in_password_reset_link(self):
        url = reverse('password-reset')
        response = self.client.post(url, {'email': 'rahman.s@e360africa.com'}, format='json')

        reset_link = response.json()[:-2]
        reset_response = self.client.get(reset_link)
        self.assertEqual(reset_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(reset_response, 'Verification token is invalid or has expired!', status_code=400)

    def test_invalid_case_use_reset_link_after_setting_new_password(self):
        url = reverse('password-reset')
        response = self.client.post(url, {'email': 'rahman.s@e360africa.com'}, format='json')

        reset_link = response.json()
        reset_response = self.client.get(reset_link)
        self.assertEqual(reset_response.status_code, status.HTTP_200_OK)

        user = get_user_model().objects.get(email='rahman.s@e360africa.com')
        user.set_password('new_password')
        user.save()

        new_reset_response = self.client.get(reset_link)
        self.assertEqual(new_reset_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(new_reset_response, 'Verification token is invalid or has expired!', status_code=400)

    def test_invalid_case_reuse_reset_link_after_login(self):
        url = reverse('password-reset')
        response = self.client.post(url, {'email': 'rahman.s@e360africa.com'}, format='json')

        reset_link = response.json()
        reset_response = self.client.get(reset_link)
        self.assertEqual(reset_response.status_code, status.HTTP_200_OK)

        user = get_user_model().objects.get(email='rahman.s@e360africa.com')
        user.set_password('new_password')
        user.save()

        url = reverse('token-obtain-pair')
        data = {
            'email': 'rahman.s@e360africa.com',
            'password': 'new_password'
        }
        response = self.client.post(url, data, format='json')
        token = response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        new_reset_response = self.client.get(reset_link)
        self.assertEqual(new_reset_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(new_reset_response, 'Verification token is invalid or has expired!', status_code=400)