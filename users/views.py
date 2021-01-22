from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.views import default_token_generator
from django.contrib.auth.signals import user_logged_in
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Department, Role
from .serializers import (EmployeeSerializer, EmployeeFullSerializer, DepartmentSerializer, RoleSerializer,
                         MyTokenObtainPairSerializer, PasswordChangeSerializer)

# Create your views here

class MyTokenObtainPairView(TokenObtainPairView):
    '''
    Send logged_in signal
    '''
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        user_id = response.data.get('user')["id"]
        user = get_user_model().objects.get(pk=user_id)
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        return response

class EmployeeList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = get_user_model().objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EmployeeFullSerializer
        return EmployeeSerializer


class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return get_user_model().objects.filter(is_active=True)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EmployeeFullSerializer
        return EmployeeSerializer


class EmployeeActivation(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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


class PasswordResetRequest(APIView):
    mail_context = {
        'subject': 'Password Reset on Flexiwork',
        'from': 'internal@e360africa.com',
        'cc': ['cc@e360africa.com']
    }
    
    def post(self, request, *args, **kwargs):
        qs = get_user_model().objects.all()
        employee_email = request.data.get('email', None)
        employee = get_object_or_404(qs, email=employee_email)
        if not employee.is_active:
            raise NotFound('This email is inactive', 'inactive_user')
        else:
            token = default_token_generator.make_token(employee)
            uid = urlsafe_base64_encode(force_bytes(employee.pk))
            reset_link = request.build_absolute_uri(reverse('password-reset-confirm', kwargs={'uid64':uid, 'token':token}))
            
            email_body = 'Your password request was succesful. Click on the Verification link {} to proceed'.format(reset_link)
            email_recipient = [employee_email]
            email = EmailMessage(
                self.mail_context['subject'],
                email_body,
                self.mail_context['from'],
                email_recipient,
                cc = self.mail_context['cc']
            )
            email.send()

            return Response({"reset_link": reset_link}, status=status.HTTP_200_OK)


class PasswordResetConfirm(APIView):
    def get(self, request, *args, **kwargs):
        qs = get_user_model().objects.all()
        uid64 = kwargs.get('uid64')
        token = kwargs.get('token')

        uid = urlsafe_base64_decode(uid64).decode()

        employee = get_object_or_404(qs, pk=uid)
        if not employee.is_active:
            raise NotFound('This email is inactive', 'inactive_user')
        else:
            token_valid = default_token_generator.check_token(employee, token)
            if not token_valid:
                raise ParseError('Verification token is invalid or has expired!')
            
            payload = {
                'user_id': employee.pk,
                'message': 'Valid verification link'
            }

            return Response(payload, status.HTTP_200_OK)


class PasswordChange(APIView):
    def post(self, request, *args, **kwargs):
        qs = get_user_model().objects.all()
        user_id = request.data.pop('user_id')
        user = get_object_or_404(qs, pk=user_id)
        if not user.is_active:
            raise NotFound('This email is inactive', 'inactive_user')
    
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['password1']
        
        user.set_password(new_password)
        user.save()

        return Response('Password Changed successfully', status.HTTP_200_OK)


class DepartmentList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentDetail(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class RoleList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleDetail(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer