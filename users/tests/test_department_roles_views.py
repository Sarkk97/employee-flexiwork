from django.urls import reverse
from django.core.files import File
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Department, Role
from ..serializers import EmployeeSerializer


class DepartmentViewTest(APITestCase):
    def setUp(self):
        d = Department.objects.create(name="Human Resources")
        Department.objects.create(name="Projects")

        user_1 = {
            'email': "rahman.s@e360africa.com",
            'first_name': 'Rahman',
            'last_name': 'Solanke',
            'department': d,
            'staff_no': 'EMP-001',
            'description': 'A good software engineer'
        }
        get_user_model().objects.create_user(**user_1)
        self.authenticator()

    def authenticator(self):
        url = reverse('login')
        data = {
            'email': 'rahman.s@e360africa.com',
            'password': 'password'
        }
        response = self.client.post(url, data, format='json')
        token = response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    
    def test_department_create(self):
        url = reverse('department-list')
        response = self.client.post(url, {"name": "Technology"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["name"], "Technology")

    def test_department_list(self):
        url = reverse('department-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)

    def test_get_department(self):
        url = reverse('department-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "Human Resources")

    def test_update_department(self):
        url = reverse('department-detail', kwargs={'pk': 1})
        response = self.client.patch(url, {"name": "Human Resources and Admin"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "Human Resources and Admin")


class RoleViewTest(APITestCase):
    def setUp(self):
        r = Role.objects.create(name="Admin")
        d = Department.objects.create(name="Projects")

        user_1 = {
            'email': "rahman.s@e360africa.com",
            'first_name': 'Rahman',
            'last_name': 'Solanke',
            'role': r,
            'department': d,
            'staff_no': 'EMP-001',
            'description': 'A good software engineer'
        }
        get_user_model().objects.create_user(**user_1)
        self.authenticator()

    def authenticator(self):
        url = reverse('login')
        data = {
            'email': 'rahman.s@e360africa.com',
            'password': 'password'
        }
        response = self.client.post(url, data, format='json')
        token = response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
    
    def test_role_create(self):
        url = reverse('role-list')
        response = self.client.post(url, {"name": "Staff"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["name"], "Staff")

    def test_role_list(self):
        url = reverse('role-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_get_role(self):
        url = reverse('role-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "Admin")

    def test_update_role(self):
        url = reverse('role-detail', kwargs={'pk': 1})
        response = self.client.patch(url, {"name": "Super Admin"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], "Super Admin")
        