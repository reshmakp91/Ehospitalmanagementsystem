from django import forms
from adminapp.models import *
from multiselectfield import MultiSelectFormField

class BookAppointment(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'reason',]
