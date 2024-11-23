from django import forms
from adminapp.models import *
from multiselectfield import MultiSelectFormField

class PatientProfileForm(forms.ModelForm):

    class Meta:

        model = PatientProfile
        fields = ['name','date_of_birth','user_type','gender','contact','email','address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        if 'date_of_birth' in self.fields:
            self.fields['date_of_birth'].widget.attrs.update({'placeholder': 'yyyy-mm-dd'})


class DoctorProfileForm(forms.ModelForm):

    class Meta:
        model = DoctorProfile
        fields =  fields = ['name', 'facility', 'user_type','contact', 'email', 'specialization', 'image']

    def __init__(self, *args, **kwargs):
        selected_facility = kwargs.pop('selected_facility', None)
        super().__init__(*args, **kwargs)
        if selected_facility:
            facility = Facility.objects.filter(id=selected_facility).first()
            if facility:
                self.fields['specialization'].choices = [
                    (dept, dept) for dept in facility.departments
                ]
            else:
                self.fields['specialization'].choices = []
        else:
            self.fields['specialization'].choices = []

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class Facilityform(forms.ModelForm):

    class Meta:

        model = Facility
        fields = '__all__'


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = '__all__'






