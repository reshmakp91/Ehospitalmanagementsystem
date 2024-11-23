from django.urls import path
import accountsapp.views
from accountsapp.views import *
import adminapp.views
from adminapp.views import *

urlpatterns = [
    path('test/', test_view, name='test'),
    path('admin/', adminapp.views.adminpanel, name='admin_dashboard'),
    path('patientcreate/', adminapp.views.patientcreate, name='patientcreate'),
    path('doctorcreate/', adminapp.views.doctorcreate, name='doctorcreate'),
    path('facilitycreate/', adminapp.views.facilitycreate, name='facilitycreate'),
    path('facilities/', adminapp.views.facilities, name='facilities'),
    path('doctors/', adminapp.views.doctors, name='doctors'),
    path('edit_doctor/<int:id>/', edit_doctor, name='edit_doctor'),
    path('patients/', adminapp.views.patients, name='patients'),
    path('appointments/', adminapp.views.appointments, name='appointments'),
    path('facility_detail/<int:facility_id>/', adminapp.views.facility_detail, name='facility_detail'),
    path('appointment_detail/<int:id>/', adminapp.views.appointment_detail, name='appointment_detail'),
    path('patient_detail/<int:patient_id>/', adminapp.views.patient_detail, name='patient_detail'),
    path('edit_patient/<int:patient_id>/', adminapp.views.edit_patient, name='edit_patient'),
    path('edit_appointment/<int:id>/', adminapp.views.edit_appointment, name='edit_appointment'),
    path('edit_facility/<int:id>/', adminapp.views.edit_facility, name='edit_facility'),
    path('medicalhistories/', adminapp.views.MedicalHistoryPatientList, name='medical_patients'),
    path('medical_list/<int:patient_id>/', adminapp.views.MedicalHistory_List, name='medical_histories'),
    path('medical_doctors/<int:doctor_id>/<int:patient_id>/', adminapp.views.View_Medical_History, name='view_medical_history'),
    path('payments/', adminapp.views.payments, name='payments'),
    path('logout/', accountsapp.views.user_logout, name='logout'),

]
