# Generated by Django 4.2.16 on 2024-11-16 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctorapp', '0002_medicalhistory_appointment_medicalhistory_doctor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicalhistory',
            name='diagnosis',
        ),
    ]
