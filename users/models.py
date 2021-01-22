from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import CustomUserManager
from .utils import CustomFileStorage

# Create your models here.
def custom_avatar_upload(instance, filename):
    return 'avatars/staff_{0}/{1}'.format(instance.staff_no, filename)

class Employee(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    staff_no = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to=custom_avatar_upload, blank=True, storage=CustomFileStorage())
    description = models.TextField(blank=True)
    department = models.ForeignKey('Department', models.SET_NULL, null=True, related_name="employees")
    role = models.ForeignKey('Role', models.SET_NULL, null=True, related_name="employees")
    date_registered = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.first_name+' '+self.last_name or self.email


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name