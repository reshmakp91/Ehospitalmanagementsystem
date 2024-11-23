from django import forms
from adminapp.models import *
from doctorapp.models import *
from multiselectfield import MultiSelectFormField

class MedicalForm(forms.ModelForm):

    class Meta:

        model = MedicalHistory
        fields = ['patient','diagnosis','treatment_description','notes']

class HealthArticleForm(forms.ModelForm):

    class Meta:

        model = HealthArticle
        fields = ['title','image','content']