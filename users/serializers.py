from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Employee, Department, Role


class DepartmentSerializer(serializers.ModelSerializer):
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        exclude = ('date_created',)

    def get_employee_count(self, obj):
        return obj.employees.count()


class RoleSerializer(serializers.ModelSerializer):
    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = '__all__'

    def get_employee_count(self, obj):
        return obj.employees.count()


class DepartmentPartialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        exclude = ('date_created',)


class RolePartialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    department = DepartmentPartialSerializer(read_only=True)
    role = RolePartialSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), write_only=True, allow_null=True, source='department')
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), write_only=True, allow_null=True, source='role')
    
    class Meta:
        model = Employee

        fields = ['id','email', 'first_name', 'last_name', 'staff_no', 'avatar',
                'department','department_id','role', 'role_id','description']
        extra_kwargs = {'id': {'read_only': True}}


    '''
    overwrite create method to use create_users for user objects so as to 
    use password hashing
    '''
    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)
    

class EmployeeFullSerializer(serializers.ModelSerializer):
    department = DepartmentPartialSerializer(read_only=True)
    role = RolePartialSerializer(read_only=True)

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
        data.update({'user': EmployeeFullSerializer(self.user).data})

        return data


class PasswordChangeSerializer(serializers.Serializer):
    password1 = serializers.CharField(max_length=100)
    password2 = serializers.CharField(max_length=100)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Password1 and Password2 must match!")
        return data
