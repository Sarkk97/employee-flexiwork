from django.urls import path

from .views import ClockTypeList, ClockList, CheckClockForEmployee, EmployeeClockOut


urlpatterns = [
    path('clocking_types', ClockTypeList.as_view(), name='clocking-types'),
    path('attendance', ClockList.as_view(), name='attendance-list'),
    path('attendance/employee/<int:pk>/confirm', CheckClockForEmployee.as_view(), name='check-employee-attendance'),
    path('attendance/employee/<int:pk>/clock_out', EmployeeClockOut.as_view(), name='attendance-clock-out')
]