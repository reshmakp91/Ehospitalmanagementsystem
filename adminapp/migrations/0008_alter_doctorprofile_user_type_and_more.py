# Generated by Django 4.2.16 on 2024-11-18 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0007_payment_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorprofile',
            name='user_type',
            field=models.CharField(blank=True, choices=[('Patient', 'Patient'), ('Doctor', 'Doctor'), ('Admin', 'Admin'), ('Pharmacy', 'Pharmacy')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='user_type',
            field=models.CharField(blank=True, choices=[('Patient', 'Patient'), ('Doctor', 'Doctor'), ('Admin', 'Admin'), ('Pharmacy', 'Pharmacy')], max_length=10, null=True),
        ),
    ]
