# Generated by Django 2.2.11 on 2020-04-04 10:22

import clocking.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClockTypes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Clock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clock_in_timestamp', models.DateTimeField(auto_now_add=True)),
                ('expected_clock_out_timestamp', models.DateTimeField(blank=True, null=True)),
                ('clock_out_timestamp', models.DateTimeField(blank=True, default=None, null=True)),
                ('clock_in_latitude', models.CharField(blank=True, max_length=50)),
                ('clock_in_longitude', models.CharField(blank=True, max_length=50)),
                ('clock_out_latitude', models.CharField(blank=True, max_length=50)),
                ('clock_out_longitude', models.CharField(blank=True, max_length=50)),
                ('clock_in_address', models.CharField(blank=True, max_length=100)),
                ('clock_out_address', models.CharField(blank=True, max_length=100)),
                ('clock_in_image', models.ImageField(blank=True, upload_to=clocking.models.clock_in_image_upload)),
                ('clock_out_image', models.ImageField(blank=True, upload_to=clocking.models.clock_out_image_upload)),
                ('clock_in_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clocking.ClockTypes')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
