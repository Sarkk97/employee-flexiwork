from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ParseError
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .serializers import EmployeeSerializer, EmployeeFullSerializer

# Create your views here.
class EmployeeList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = get_user_model().objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EmployeeFullSerializer
        return EmployeeSerializer


class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    #authentication_classes = []
    permission_classes = []
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return get_user_model().objects.filter(is_active=True)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EmployeeFullSerializer
        return EmployeeSerializer

class EmployeeActivation(APIView):
    #authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        activation_status = request.data.get('action', None)
        if activation_status is None:
            raise ParseError("'action' key missing from post body. Value should be either activate or deactivate", status.HTTP_400_BAD_REQUEST)
        employee = get_object_or_404(get_user_model(), pk=pk)
        if activation_status == 'activate':
            employee.is_active = True
        elif activation_status == 'deactivate':
            employee.is_active = False
        else:
            raise ParseError('invalid options for activation. Value should be either activate or deactivate')
        employee.save()
        serializer = EmployeeFullSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)