from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee

        fields = ['id','email', 'first_name', 'last_name', 'staff_no', 'avatar',
                'description']
        extra_kwargs = {'id': {'read_only': True}}

    '''
    overwrite create method to use create_users for user objects so as to 
    use password hashing
    '''
    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)
    

class EmployeeFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ('password',)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    '''
    DRF simple-jwt does not update user last login after getting a new token.
    Fix is to subclass the TokenObtainPairSerializer and add the user_id to the
    serializer response data
    '''
    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        data.update({'user_id': self.user.pk})
        return data
