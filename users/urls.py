from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import (EmployeeList, EmployeeDetail, EmployeeActivation, MyTokenObtainPairView,
                    PasswordResetRequest, PasswordResetConfirm)

urlpatterns = [
    path('auth/token', MyTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/password-reset', PasswordResetRequest.as_view(), name='password-reset'),
    path('auth/password-reset-confirm/<uid64>/<token>', PasswordResetConfirm.as_view(), name='password-reset-confirm'),

    path('employees', EmployeeList.as_view(), name='employee-list'),
    path('employees/<int:pk>', EmployeeDetail.as_view(), name='employee-detail'),
    path('employee/<int:pk>/activation', EmployeeActivation.as_view(), name='employee-activation')

]