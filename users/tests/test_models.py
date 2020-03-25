from django.test import TestCase
from django.core.files import File

from ..models import Employee

class UserCreateModelTest(TestCase):
    """
    Test module for user model exists
    """
    def test_can_create_user_in_db(self):
        user = Employee.objects.create(email="rahman.s@e360africa.com", first_name="Rahman", last_name="Solanke")
        self.assertIsNotNone(user)

class EmployeeModelTest(TestCase):
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

        user_1 = Employee(**user_1)
        user_1.avatar.save('rahman.png', File(open(user_1_img, 'rb')))

        user_2 = Employee(**user_2)
        user_2.avatar.save('ahmed.png', File(open(user_2_img, 'rb')))

    def test_users_created(self):
        self.assertEqual(Employee.objects.count(), 2)
    
    def test_users_details(self):
        user_1 = Employee.objects.get(pk=1)
        user_2 = Employee.objects.get(pk=2)
        self.assertEqual(user_1.email, 'rahman.s@e360africa.com')
        self.assertEqual(user_2.email, 'ahmed.o@e360africa.com')
        self.assertTrue(user_1.is_active)
        self.assertTrue(user_2.is_active)
        self.assertEqual(user_1.first_name, 'Rahman')
        self.assertEqual(user_2.last_name, 'Ojo')
        self.assertIsNone(user_1.last_login)