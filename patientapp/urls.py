from django.urls import path
from accountsapp import views as accounts_views
from doctorapp import views as doctor_views
from patientapp import views as patient_views
import accountsapp.views
from accountsapp.views import *

urlpatterns = [
    path('patient/', patient_views.patient_dashboard, name='patient_dashboard'),
    path('new_appointment/',patient_views.new_appointment,name='pat_new_appointment'),
    path('appointment_detail/<int:id>/',patient_views.appointment_detail,name='pat_appointment_detail'),
    path('logout/', accounts_views.user_logout, name='logout'),
    path('appointments/',patient_views.appointments, name='pat_appointments'),
    path('checkout_session/<int:appointment_id>/', patient_views.checkout_session, name='checkout_session'),
    path('payment_success/<int:appointment_id>/', patient_views.payment_success, name='payment_success'),
    path('edit_appointment/<int:id>/', patient_views.edit_appointment, name='pat_edit_appointment'),
    path('medical_history_list/',patient_views.MedicalHistoryList,name='medicallist'),
    path('medical_history/<int:doctor_id>/',patient_views.View_Medical,name='view_medical_history'),
    path('eprescriptions/',patient_views.ViewPrescriptions,name='view_prescriptions'),
    path('view_profile/',patient_views.view_profile,name='view_profile'),
    path('edit_profile/', patient_views.edit_profile, name='edit_profile'),

]
