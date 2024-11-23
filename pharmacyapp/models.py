from django.db import models
from doctorapp.models import Prescription

class PharmacyModel(models.Model):

    prescription = models.ForeignKey(Prescription,on_delete=models.CASCADE,null=True, blank=True)
    availability_status = models.CharField(max_length=25,choices=[('In-stock','In-stock'),('out-of-stock','out-of-stock')])

    def __str__(self):
        return f"{self.prescription}-{self.availability_status}"