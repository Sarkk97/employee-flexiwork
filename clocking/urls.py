from django.urls import path

from .views import ClockTypeList, ClockList, CheckClockForEmployee, EmployeeClockOut


urlpatterns = [
    path('clocking_types', ClockTypeList.as_view(), name='clocking-types'),
    path('attendance', ClockList.as_view(), name='attendance-list'),
    path('attendance/confirm/<int:pk>', CheckClockForEmployee.as_view(), name='check-employee-attendance'),
    path('attendance/clock_out/<int:pk>', EmployeeClockOut.as_view(), name='attendance-clock-out')
]