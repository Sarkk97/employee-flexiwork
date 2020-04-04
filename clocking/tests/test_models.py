import datetime
from unittest import skip

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from ..models import Clock, ClockType


class TestClockTypesModel(APITestCase):
    def test_can_create_clock_tyoes(self):
        ClockType.objects.create(name="Office")
        ClockType.objects.create(name="Remote")
        ClockType.objects.create(name="Onsite")

        self.assertEqual(ClockType.objects.count(), 3)
        self.assertEqual(ClockType.objects.get(pk=2).name, "Remote")


class TestClockModel(APITestCase):
    def setUp(self):
        self.clock_type = ClockType.objects.create(name="Office")
        self.user = get_user_model().objects.create_user(email="rahman.s@e360africa.com", first_name="Rahman", last_name="Solanke")
    
    def test_can_create_clocking_object(self):
        #Create clock object
        clock_object = Clock.objects.create(
            employee = self.user,
            clock_in_type = self.clock_type,
        )
        self.assertIsNotNone(clock_object)
        clock_object.expected_clock_out_timestamp = clock_object.clock_in_timestamp + datetime.timedelta(hours=8)
        clock_object.save()
        
        self.assertEqual(Clock.objects.count(), 1)
        self.assertEqual(Clock.objects.get(pk=1).overtime, "N/A")


class TestClockObjectLogic(APITestCase):
    def setUp(self):
        clock_type = ClockType.objects.create(name="Office")
        user = get_user_model().objects.create_user(email="rahman.s@e360africa.com", first_name="Rahman", last_name="Solanke")
        clock_object = Clock.objects.create(
            employee = user,
            clock_in_type = clock_type,
        )
        clock_object.expected_clock_out_timestamp = clock_object.clock_in_timestamp + datetime.timedelta(hours=8)
        clock_object.save()

    def test_correct_clock_object_employee(self):
        clock_obj = Clock.objects.get(pk=1)
        self.assertEqual(clock_obj.employee.id, 1)
        self.assertEqual(clock_obj.employee.email, "rahman.s@e360africa.com")

    def test_correct_clock_object_type(self):
        clock_obj = Clock.objects.get(pk=1)
        self.assertEqual(clock_obj.clock_in_type.id, 1)
        self.assertEqual(clock_obj.clock_in_type.name, "Office")
    
    def test_correct_clock_in_time(self):
        clock_obj = Clock.objects.get(pk=1)
        self.assertIsNotNone(clock_obj.clock_in_timestamp)
        self.assertIsInstance(clock_obj.clock_in_timestamp, datetime.datetime)

    def test_correct_expected_clock_out_time(self):
        clock_obj = Clock.objects.get(pk=1)
        self.assertIsNotNone(clock_obj.expected_clock_out_timestamp)
        self.assertIsInstance(clock_obj.expected_clock_out_timestamp, datetime.datetime)
        self.assertEqual(clock_obj.expected_clock_out_timestamp, clock_obj.clock_in_timestamp + datetime.timedelta(hours=8))

        self.assertIsNone(clock_obj.clock_out_timestamp)
        self.assertEqual(clock_obj.overtime, "N/A")

    def test_correct_clock_out_time(self):
        clock_obj = Clock.objects.get(pk=1)
        clock_obj.clock_out_timestamp = clock_obj.expected_clock_out_timestamp + datetime.timedelta(hours=1, minutes=30, seconds=20)
        clock_obj.save()

        clock_obj = Clock.objects.get(pk=1)
        self.assertIsNotNone(clock_obj.clock_out_timestamp)
        self.assertEqual(clock_obj.overtime, [1, 30, 20])
        