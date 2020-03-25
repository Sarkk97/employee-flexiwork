
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import CustomUserManager

# Create your models here.
class Employee(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    staff_no = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    description = models.TextField(blank=True)
    #department = models.ForeignKey('Department', models.SET_NULL, null=True)
    date_registered = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.first_name+' '+self.last_name or self.email
    
