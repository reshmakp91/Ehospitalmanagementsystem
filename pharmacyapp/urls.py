import pharmacyapp.views
from django.urls import path
from pharmacyapp.views import *
from accountsapp.views import *
import accountsapp.views

urlpatterns = [

    path('pharmacyview/',pharmacyapp.views.pharmacy_list,name='pharmacy_list'),
    path('logout/', accountsapp.views.user_logout, name='logout'),
    path('update_status/<int:item_id>/',pharmacyapp.views.update_status,name='update_medication_status'),

]