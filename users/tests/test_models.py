from django.test import TestCase
from django.core.files import File
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from ..models import Department, Role
from ..serializers import EmployeeSerializer


class UserCreateModelTest(APITestCase):
    """
    Test module for user model exists
    """
    def test_can_create_user_in_db(self):
        user = get_user_model().objects.create_user(email="rahman.s@e360africa.com", first_name="Rahman", last_name="Solanke")
        self.assertIsNotNone(user)


class DepartmentCreateModelTest(APITestCase):
    def test_can_create_department(self):
        self.assertIsNotNone(Department.objects.create(name="Technology"))
        self.assertEqual(Department.objects.count(), 1)
        dept = Department.objects.get(pk=1)
        self.assertEqual(dept.name, "Technology")


class RoleCreateModelTest(APITestCase):
    def test_can_create_role(self):
        self.assertIsNotNone(Role.objects.create(name="Admin"))
        self.assertEqual(Role.objects.count(), 1)
        role = Role.objects.get(pk=1)
        self.assertEqual(role.name, "Admin")


class EmployeeModelTest(APITestCase):
    """
    Test module for Employee Model functionality
    """
    def setUp(self):
        user_1 = {
            'email': "rahman.s@e360africa.com",
            'first_name': 'Rahman',
            'last_name': 'Solanke',
            'staff_no': 'EMP-001',
            'description': 'A good software engineer'
        }
        user_1_img = '/home/rahman/Pictures/Naija.png'

        user_2 = {
            'email': "ahmed.o@e360africa.com",
            'first_name': 'Ahmed',
            'last_name': 'Ojo',
            'staff_no': 'EMP-002',
            'description': 'A good software engineer'
        }
        user_2_img = '/home/rahman/Pictures/Naija2.png'

        user_1 = get_user_model().objects.create_user(**user_1)
        user_1.avatar.save('rahman.png', File(open(user_1_img, 'rb')))

        user_2 = get_user_model().objects.create_user(**user_2)
        user_2.avatar.save('ahmed.png', File(open(user_2_img, 'rb')))

    def test_users_created(self):
        self.assertEqual(get_user_model().objects.count(), 2)
    
    def test_users_details(self):
        user_1 = get_user_model().objects.get(pk=1)
        user_2 = get_user_model().objects.get(pk=2)
        self.assertEqual(user_1.email, 'rahman.s@e360africa.com')
        self.assertEqual(user_2.email, 'ahmed.o@e360africa.com')
        self.assertTrue(user_1.is_active)
        self.assertTrue(user_2.is_active)
        self.assertEqual(user_1.first_name, 'Rahman')
        self.assertEqual(user_2.last_name, 'Ojo')
        self.assertIsNone(user_1.last_login)
        self.assertTrue(user_1.check_password('password'))


class EmployeeDepartmentTest(APITestCase):
    def setUp(self):
        Department.objects.create(name="Technology")
        Role.objects.create(name="Admin")

        self.user_1 = {
            'email': "rahman.s@e360africa.com",
            'first_name': 'Rahman',
            'last_name': 'Solanke',
            'role_id': 1,
            'department_id': 1,
            'staff_no': 'EMP-001',
            'description': 'A good software engineer'
        }

        get_user_model().objects.create_user(**self.user_1)
    
    def test_employee_detailed_serializer(self):
        emp = get_user_model().objects.get(pk=1)
        serializer =  EmployeeSerializer(emp)
        self.assertIsNotNone(serializer.data)