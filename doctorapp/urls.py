import accountsapp.views
import doctorapp.views
from django.urls import path
from . import views
from adminapp.views import *
from doctorapp.views import *
import accountsapp.views
from accountsapp.views import *
from .views import *

urlpatterns = [

    path('doctor/',views.doctor_dashboard,name='doctor_dashboard'),
    path('appointment_detail/<int:id>/',doctorapp.views.appointment_detail,name='doc_appointment_detail'),
    path('appointments/',doctorapp.views.appointments, name='doc_appointments'),
    path('logout/', accountsapp.views.user_logout, name='logout'),
    path('patients/',doctorapp.views.patients,name='my_patients'),
    path('patient_detail/<int:patient_id>/',doctorapp.views.patient_detail, name='doc_patient_detail'),
    path('edit_appointment/<int:id>/', doctorapp.views.edit_appointment, name='doc_edit_appointment'),
    path('update_medical/<int:appointment_id>/',doctorapp.views.update_MedicalDetails,name='update_medical'),
    path('medical_patients_list/',doctorapp.views.MedicalHistoryPatientList,name='medicalpatients'),
    path('medical_history/<int:patient_id>/',doctorapp.views.ViewMedicalHistory,name='medical_history'),
    path('edit_prescription/<int:appointment_id>/',doctorapp.views.edit_prescription,name='edit_prescription'),
    path('eprescriptions/',doctorapp.views.view_prescriptions,name='eprescriptions'),
    path('new_article/',doctorapp.views.upload_article,name='new_article'),
    path('send_to_pharmacy/<int:prescription_id>/',doctorapp.views.send_to_pharmacy,name='send_to_pharmacy'),
]