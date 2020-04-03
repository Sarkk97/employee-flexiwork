from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import (EmployeeList, EmployeeDetail, EmployeeActivation, MyTokenObtainPairView,
                    PasswordResetRequest, PasswordResetConfirm, PasswordChange, DepartmentList,
                    DepartmentDetail, RoleList, RoleDetail)

urlpatterns = [
    path('employees', EmployeeList.as_view(), name='employee-list'),
    path('employee/<int:pk>', EmployeeDetail.as_view(), name='employee-detail'),
    path('employee/<int:pk>/activation', EmployeeActivation.as_view(), name='employee-activation'),
    path('departments', DepartmentList.as_view(), name='department-list'),
    path('department/<int:pk>', DepartmentDetail.as_view(), name='department-detail'),
    path('roles', RoleList.as_view(), name='role-list'),
    path('role/<int:pk>', RoleDetail.as_view(), name='role-detail'),
    path('auth/login', MyTokenObtainPairView.as_view(), name='login'),
    path('auth/token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('auth/password-reset', PasswordResetRequest.as_view(), name='password-reset'),
    path('auth/password-reset-confirm/<uid64>/<token>', PasswordResetConfirm.as_view(), name='password-reset-confirm'),
    path('auth/password-change', PasswordChange.as_view(), name='password-change')

]