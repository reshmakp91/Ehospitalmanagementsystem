# Generated by Django 4.2.16 on 2024-11-16 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0006_alter_appointment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='appointment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adminapp.appointment'),
        ),
    ]
