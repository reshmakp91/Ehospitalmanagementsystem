from django.db import models
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User


DEPARTMENT_CHOICES = [
    ('Cardiology', 'Cardiology'),
    ('Neurology', 'Neurology'),
    ('Pediatrics', 'Pediatrics'),
    ('Radiology', 'Radiology'),
    ('Orthopedics', 'Orthopedics'),
    ('Gynecology','Gynecology')
]

RESOURCE_CHOICES = [
    ('MRI Machine', 'MRI Machine'),
    ('CT Scanner', 'CT Scanner'),
    ('X-Ray Machine', 'X-Ray Machine'),
    ('Ultrasound', 'Ultrasound'),
    ('Blood Testing Lab', 'Blood Testing Lab'),
    ('Pharmacy', 'Pharmacy'),
    ('ECG','ECG'),
    ('Transport Services','Transport Services')
]

USER_TYPE_CHOICES = [
    ('Patient', 'Patient'),
    ('Doctor', 'Doctor'),
    ('Admin','Admin'),
    ('Pharmacy','Pharmacy')
]

class AdminProfile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.user_type

class PharmacyProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.user_type

class PatientProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Facility(models.Model):

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=[('Hospital', 'Hospital'), ('Clinic', 'Clinic')], default=[])
    departments = MultiSelectField(choices=DEPARTMENT_CHOICES, default=[])
    resources = MultiSelectField(choices=RESOURCE_CHOICES, default=[])
    image = models.ImageField(upload_to='facilities/',null=True, blank=True)

    def __str__(self):
        return self.name

class DoctorProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES,null=True, blank=True)
    facility = models.ForeignKey(Facility,on_delete=models.CASCADE)
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    specialization = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    image = models.ImageField(upload_to='Doctors/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" {self.name}"

class Appointment(models.Model):

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, null=True)
    appointment_date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=50, choices=[
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('Pending Payment','Pending Payment')
    ])

    def __str__(self):
        return f"Appointment for {self.patient.name} with {self.doctor.name} on {self.appointment_date}"

class Payment(models.Model):

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE,null=True)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name} - {self.amount}"

