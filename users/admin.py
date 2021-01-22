from django.contrib import admin

# Register your models here.
email = 'rahman@email.com'
first = ''
last = ''
def fullname():
    return first+last or email