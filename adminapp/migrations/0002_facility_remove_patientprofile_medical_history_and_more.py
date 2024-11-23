# Generated by Django 4.2.16 on 2024-11-11 11:34

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('Hospital', 'Hospital'), ('Clinic', 'Clinic')], default=[], max_length=10)),
                ('departments', multiselectfield.db.fields.MultiSelectField(choices=[('Cardiology', 'Cardiology'), ('Neurology', 'Neurology'), ('Pediatrics', 'Pediatrics'), ('Radiology', 'Radiology'), ('Orthopedics', 'Orthopedics'), ('Gynecology', 'Gynecology')], default=[], max_length=64)),
                ('resources', multiselectfield.db.fields.MultiSelectField(choices=[('MRI Machine', 'MRI Machine'), ('CT Scanner', 'CT Scanner'), ('X-Ray Machine', 'X-Ray Machine'), ('Ultrasound', 'Ultrasound'), ('Blood Testing Lab', 'Blood Testing Lab'), ('Pharmacy', 'Pharmacy'), ('ECG', 'ECG'), ('Transport Services', 'Transport Services')], default=[], max_length=97)),
                ('image', models.ImageField(blank=True, null=True, upload_to='facilities/')),
            ],
        ),
        migrations.RemoveField(
            model_name='patientprofile',
            name='medical_history',
        ),
        migrations.AddField(
            model_name='doctorprofile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='Doctors/'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adminapp.doctorprofile'),
        ),
        migrations.AlterField(
            model_name='doctorprofile',
            name='specialization',
            field=models.CharField(choices=[('Cardiology', 'Cardiology'), ('Neurology', 'Neurology'), ('Pediatrics', 'Pediatrics'), ('Radiology', 'Radiology'), ('Orthopedics', 'Orthopedics'), ('Gynecology', 'Gynecology')], max_length=100),
        ),
        migrations.AlterField(
            model_name='doctorprofile',
            name='facility',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.facility'),
        ),
    ]
