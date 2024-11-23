from django.db import models
from adminapp.models import *
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

class MedicalHistory(models.Model):

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='medical_history')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE,null=True)
    diagnosis = models.CharField(max_length=255, null=True)
    treatment_description = models.TextField(null=True)
    appointment = models.ForeignKey(Appointment,on_delete=models.CASCADE,null=True)
    date = models.DateField()
    notes = models.TextField()

    def __str__(self):
        return f"{self.diagnosis} - {self.patient.name}"


class Prescription(models.Model):

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    medical =models.ForeignKey(MedicalHistory,on_delete=models.CASCADE,null=True)
    medication = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)
    prescribed_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient.name} by {self.doctor.name}"

class HealthArticle(models.Model):

    title = models.CharField(max_length=200,null=True, blank=True)
    image = models.ImageField(upload_to='article_images/', null=True, blank=True)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='uploaded_articles')
    content = models.TextField(null=True, blank=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} by {self.doctor.name}"

