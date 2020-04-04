from datetime import datetime, timedelta

from django.db import models
from django.conf import settings


def clock_in_image_upload(instance, filename):
    _now = datetime.now()
    return 'clock_in/staff_{staff_num}/{year}_{month}_{day}_{name}'.format(staff_num=instance.staff_no, name=filename,
                                        year=_now.strftime("%Y"), month=_now.strftime("%m"), day=_now.strftime("%d"))

def clock_out_image_upload(instance, filename):
    _now = datetime.now()
    return 'clock_out/staff_{staff_num}/{year}_{month}_{day}_{name}'.format(staff_num=instance.staff_no, name=filename,
                                        year=_now.strftime("%Y"), month=_now.strftime("%m"), day=_now.strftime("%d"))


class Clock(models.Model):
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendance')
    clock_in_timestamp = models.DateTimeField(auto_now_add=True)
    expected_clock_out_timestamp = models.DateTimeField(blank=True, null=True)
    clock_out_timestamp = models.DateTimeField(blank=True, null=True, default=None)
    clock_in_type = models.ForeignKey('ClockType', on_delete=models.SET_NULL, null=True)
    clock_in_latitude = models.CharField(max_length=50, blank=True)
    clock_in_longitude = models.CharField(max_length=50, blank=True)
    clock_out_latitude = models.CharField(max_length=50, blank=True)
    clock_out_longitude = models.CharField(max_length=50, blank=True)
    clock_in_address = models.CharField(max_length=100, blank=True)
    clock_out_address = models.CharField(max_length=100, blank=True)
    clock_in_image = models.ImageField(upload_to=clock_in_image_upload, blank=True)
    clock_out_image = models.ImageField(upload_to=clock_out_image_upload, blank=True)
    valid_attendance = models.BooleanField(default=False)

    def get_duration(self, expected, actual):
        duration = actual - expected
        duration_in_secs = duration.total_seconds()

        h = divmod(duration_in_secs, 3600)
        m = divmod(h[1], 60)
        return [int(h[0]), int(m[0]), int(m[1])] #In form of [hour, minutes, seconds] 
    
    @property
    def overtime(self):
        if self.clock_out_timestamp:
            return self.get_duration(self.expected_clock_out_timestamp, self.clock_out_timestamp)
        else:
            return "N/A"

    def save(self, *args, **kwargs):
        #populate expected_clock_out_timestamp on first time save i.e newly created i.e no pk yet
        if not self.pk:
            super(Clock, self).save(*args, **kwargs)
            self.expected_clock_out_timestamp = self.clock_in_timestamp + timedelta(hours=8)
            self.save()
        else:
            super(Clock, self).save(*args, **kwargs)

    def __str__(self):
        return '{} {} - {}'.format(self.employee.first_name, self.employee.last_name,
                 self.clock_in_timestamp.strftime("%Y-%m-%d"))


class ClockType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

