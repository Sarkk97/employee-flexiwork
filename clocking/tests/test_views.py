from unittest import skip

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Role, Department
from ..models import Clock, ClockType


class TestClockTypeViews(APITestCase):
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

    def test_can_create_clock_type(self):
        url = reverse('clocking-types')
        data = {
            'name': 'Office'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ClockType.objects.count(), 1)
        self.assertEqual(ClockType.objects.get(pk=1).name, "Office")

    def test_can_get_clock_types(self):
        url = reverse('clocking-types')
        data_1 = {
            'name': 'Office'
        }
        data_2 = {
            'name': 'Remote'
        }
        data_3 = {
            'name': 'Onsite'
        }
        self.client.post(url, data_1, format='json')
        self.client.post(url, data_2, format='json')
        self.client.post(url, data_3, format='json')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)


class TestClockObjectViews(APITestCase):
    def setUp(self):
        ClockType.objects.create(name="Office")
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

    def test_create_new_clock_in_object(self):
        url = reverse('attendance-list')
        data = {
            'employee_id': 1,
            'clock_in_type_id': 1
        }    
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_multiple_create_new_clock_in_object(self):
        url = reverse('attendance-list')
        data = {
            'employee_id': 1,
            'clock_in_type_id': 1
        }    
        self.client.post(url, data, format='json')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_clock_objects(self):
        url = reverse('attendance-list')
        data = {
            'employee_id': 1,
            'clock_in_type_id': 1
        }  
        self.client.post(url, data, format='json')   
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
    
    def test_get_clock_objects_with_image(self):
        img_url = '/home/rahman/Pictures/Naija.png'
        url = reverse('attendance-list')

        with open(img_url, 'rb') as clock_in_img:
            data = {
                'employee_id': 1,
                'clock_in_type_id': 1,
                'clock_in_image': clock_in_img
            }
            self.client.post(url, data, format='multipart')
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
    
    def test_invalid_confirm_employee_clock_object(self):
        url = reverse('check-employee-attendance', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertContains(response, 'This Employee has not clocked in today!', status_code=404)

    def test_valid_confirm_employee_clock_object(self):
        url = reverse('attendance-list')
        data = {
            'employee_id': 1,
            'clock_in_type_id': 1
        }  
        self.client.post(url, data, format='json')

        url = reverse('check-employee-attendance', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_employee_clock_out(self):
        url = reverse('attendance-clock-out', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertContains(response, "This Employee has not clocked in today and hence can't clock out!", status_code=404)

    def test_clock_out_before_expected(self):
        url = reverse('attendance-list')
        data = {
            'employee_id': 1,
            'clock_in_type_id': 1
        }  
        self.client.post(url, data, format='json')

        url = reverse('attendance-clock-out', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, "You can't clock out yet. Expected clock out time is", status_code=400)

    @skip
    def test_valid_employee_clock_out(self):
        url = reverse('attendance-list')
        data = {
            'employee_id': 1,
            'clock_in_type_id': 1
        }  
        self.client.post(url, data, format='json')

        url = reverse('attendance-clock-out', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)