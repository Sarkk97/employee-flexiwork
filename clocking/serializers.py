from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import ClockType, Clock


class ClockTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClockType
        fields = '__all__'


class ClockSerializer(serializers.ModelSerializer):
    clock_in_type = ClockTypeSerializer(read_only=True)
    clock_in_type_id = serializers.PrimaryKeyRelatedField(queryset=ClockType.objects.all(), write_only=True, source='clock_in_type')
    employee_id = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(), write_only=True, source='employee')
    
    class Meta:
        model = Clock
        fields = ('id','employee','employee_id', 'clock_in_timestamp', 'expected_clock_out_timestamp', 'clock_out_timestamp',
                    'clock_in_type', 'clock_in_type_id', 'clock_in_latitude', 'clock_out_latitude', 'clock_in_longitude', 'clock_out_longitude',
                    'clock_in_address', 'clock_out_address', 'clock_in_image', 'clock_out_image', 'overtime')
        extra_kwargs = {
            'id': {'read_only': True},
            'clock_in_timestamp': {'read_only': True},
            'expected_clock_out_timestamp': {'read_only': True},
            'clock_out_timestamp': {'read_only': True},
            'employee': {'read_only': True}
        }

    