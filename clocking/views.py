from datetime import datetime

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound

from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import ClockType, Clock
from .serializers import ClockTypeSerializer, ClockSerializer
# Create your views here.

class ClockTypeList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ClockType.objects.all()
    serializer_class = ClockTypeSerializer


class ClockList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ClockSerializer

    def get_queryset(self):
        qs = Clock.objects.all()
        
        employee_id = self.request.query_params.get('employee', None)
        clock_in_type = self.request.query_params.get('type', None)
        start_date = self.request.query_params.get('start', None)
        end_date = self.request.query_params.get('end', None)

        if employee_id:
            qs = qs.filter(employee_id=employee_id)
        if clock_in_type:
            qs = qs.filter(clock_in_type_id=clock_in_type)
        if start_date:
            date = datetime.strptime(start_date, "%Y-%m-%d")
            qs = qs.filter(clock_in_timestamp__date__gte=date)
        if end_date:
            date = datetime.strptime(end_date, "%Y-%m-%d")
            qs = qs.filter(clock_in_timestamp__date__lte=date)

        return qs

    def perform_create(self, serializer):
        employee_id = serializer.validated_data.get('employee').pk
        #Check if employee does not have clock-in object for the day
        _date = datetime.date(datetime.now())
        clock_obj_exist = self.get_queryset().filter(clock_in_timestamp__date=_date, employee__id=employee_id).exists()
        if not clock_obj_exist:
            serializer.save()
        else:
            raise ParseError('This employee already has a registered clock-in for today!')


class CheckClockForEmployee(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        
        _date = datetime.date(datetime.now())
        try:
            clock_obj = Clock.objects.get(clock_in_timestamp__date=_date, employee__id=pk)
        except ObjectDoesNotExist:
            raise NotFound('This Employee has not clocked in today!')
    
        serializer = ClockSerializer(clock_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeClockOut(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        
        current_datetime = datetime.now()
        _date = datetime.date(current_datetime)
        try:
            clock_obj = Clock.objects.get(clock_in_timestamp__date=_date, employee__id=pk)
        except ObjectDoesNotExist:
            raise NotFound("This Employee has not clocked in today and hence can't clock out!")
        
        if current_datetime < clock_obj.expected_clock_out_timestamp:
            raise ParseError("You can't clock out yet. Expected clock out time is {}".format(clock_obj.expected_clock_out_timestamp))
        
        clock_obj.clock_out_timestamp = current_datetime
        clock_obj.valid_attendance = True   
        clock_obj.save()

        serializer = ClockSerializer(clock_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

