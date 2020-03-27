from unittest import skip

from django.urls import reverse
from django.core.files import File
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from ..serializers import EmployeeSerializer


class EmployeeCreateTests(APITestCase):
    def setUp(self):
        user_1 = {
            'email': "ahmed.o@e360africa.com",
            'first_name': 'Ahmed',
            'last_name': 'Ojo',
            'staff_no': 'EMP-002',
            'description': 'A good software engineer'
        }
        get_user_model().objects.create_user(**user_1)
        self.authenticator()

    def authenticator(self):
        url = reverse('token_obtain_pair')
        data = {
            'email': 'ahmed.o@e360africa.com',
            'password': 'password'
        }
        response = self.client.post(url, data, format='json')
        token = response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_can_create_employee(self):
        url = reverse('employee-list')
        data = {
            'email': "rahman.s@e360africa.com",
            'first_name': 'Rahman',
            'last_name': 'Solanke',
            'staff_no': 'EMP-001',
            'description': 'A good software engineer'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 2)
        self.assertEqual(get_user_model().objects.last().email, 'rahman.s@e360africa.com')
        self.assertTrue(get_user_model().objects.last().check_password('password'))

    def test_can_create_employee_with_image(self):
        img_url = '/home/rahman/Pictures/Naija.png'
        with open(img_url, 'rb') as img_file:
            url = reverse('employee-list')
            data = {
                'email': "rahman.s@e360africa.com",
                'first_name': 'Rahman',
                'last_name': 'Solanke',
                'staff_no': 'EMP-001',
                'description': 'A good software engineer',
                'avatar': img_file
            }
            response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 2)
        self.assertEqual(get_user_model().objects.last().email, 'rahman.s@e360africa.com')
        self.assertIsNotNone(get_user_model().objects.last().avatar)


class EmployeeRetrieveUpdateDeleteTests(APITestCase):

    def setUp(self):
        img_url_1 = '/home/rahman/Pictures/Naija.png'
        img_url_2 = '/home/rahman/Pictures/Naija2.png'
        img_url_3 = '/home/rahman/Pictures/naija3.png'

        data_1 = {
                'email': "rahman.s@e360africa.com",
                'first_name': 'Rahman',
                'last_name': 'Solanke',
                'staff_no': 'EMP-001',
                'description': 'A good software engineer',
            }
        data_2 = {
                'email': "ahmed.o@e360africa.com",
                'first_name': 'Ahmed',
                'last_name': 'Ojo',
                'staff_no': 'EMP-002',
                'description': 'A good software engineer',
            }
        data_3 = {
                'email': "Nonso.m@e360africa.com",
                'first_name': 'Nonso',
                'last_name': 'Mgbechi',
                'staff_no': 'EMP-003',
                'description': 'A good software engineer',
            }

        user_1 = get_user_model().objects.create_user(**data_1)
        user_1.avatar.save('rahman.png', File(open(img_url_1, 'rb')))

        user_2 = get_user_model().objects.create_user(**data_2)
        user_2.avatar.save('ahmed.png', File(open(img_url_2, 'rb')))

        user_3 = get_user_model().objects.create_user(**data_3)
        user_3.avatar.save('nonso.png', File(open(img_url_3, 'rb'))) 
        
        self.authenticator()


    def authenticator(self):
        url = reverse('token_obtain_pair')
        data = {
            'email': 'rahman.s@e360africa.com',
            'password': 'password'
        }
        response = self.client.post(url, data, format='json')
        token = response.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_get_all_employees(self):
        url = reverse('employee-list')
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_valid_employee(self):
        url = reverse('employee-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], 1)
    
    def test_get_invalid_employee(self):
        url = reverse('employee-detail', kwargs={'pk': 20})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_employee_default_password(self):
        emp = get_user_model().objects.get(pk=1)
        emp2 = get_user_model().objects.get(pk=2)
        emp3 = get_user_model().objects.get(pk=3)
        self.assertTrue(emp.check_password('password'))
        self.assertTrue(emp2.check_password('password'))
        self.assertTrue(emp3.check_password('password'))

    def test_can_not_get_inactive_employee_detail(self):
        emp = get_user_model().objects.get(pk=1)
        emp.is_active = False
        emp.save()
        url = reverse('employee-detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_update_employee(self):
        url = reverse('employee-detail', kwargs={'pk': 1})
        response = self.client.patch(url, {'description': 'Now a senior dev'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['description'], 'Now a senior dev')
    
    def test_can_do_multiple_updates_employee(self):
        url = reverse('employee-detail', kwargs={'pk': 3})
        response = self.client.patch(url, {'description': 'Now a senior dev', 'email':'Nonso.omo@e360africa.com'},
                                    format='json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['description'], 'Now a senior dev')
        self.assertEqual(data['email'], 'Nonso.omo@e360africa.com')

    def test_invalid_update_employee(self):
        url = reverse('employee-detail', kwargs={'pk': 2})
        response = self.client.patch(url, {'description': 'Now a junior dev', 'email':'ahmed.o'},
                                    format='json')
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'valid', status_code=400)


class EmployeeActivationTests(APITestCase):
    
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

        #Now pk = 1 is active while pk =2 is inactive"
    
    def test_deactivate_employee(self):
        url = reverse('employee-activation', kwargs={'pk': 1})
        response = self.client.post(url, {'action': 'deactivate'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_response = self.client.get(reverse('employee-detail', kwargs={'pk': 1}))
        self.assertEqual(new_response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_activate_employee(self):
        #pk=2 is inactive, detail api should return 404
        old_response = self.client.get(reverse('employee-detail', kwargs={'pk': 2}))
        self.assertEqual(old_response.status_code, status.HTTP_404_NOT_FOUND)

        #activate pk=2
        url = reverse('employee-activation', kwargs={'pk': 2})
        response = self.client.post(url, {'action': 'activate'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #now pk=2 should return 200
        new_response = self.client.get(reverse('employee-detail', kwargs={'pk': 2}))
        self.assertEqual(new_response.status_code, status.HTTP_200_OK)
    
    def test_invalid_activation_payload(self):
        url = reverse('employee-activation', kwargs={'pk': 1})
        response = self.client.post(url, {'anotherKey': 'deactivate'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, "'action' key missing from post body.", status_code=400)

        new_response = self.client.post(url, {'action': 'nonsense' }, format='json')
        self.assertEqual(new_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(new_response, "invalid options for activation.", status_code=400)


class RequestContext(APITestCase):
    def test_can_access_user_in_authenticated_session(self):
        pass