# Generated by Django 4.2.16 on 2024-11-16 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0007_payment_appointment'),
        ('doctorapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicalhistory',
            name='appointment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adminapp.appointment'),
        ),
        migrations.AddField(
            model_name='medicalhistory',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adminapp.doctorprofile'),
        ),
    ]
