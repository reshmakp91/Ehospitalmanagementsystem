from django.urls import path
import accountsapp.views
from accountsapp.views import *

urlpatterns = [
    path('register/patient/', accountsapp.views.patient_register, name='patient_register'),
    path('register/doctor/', accountsapp.views.doctor_register, name='doctor_register'),
    path('login/',accountsapp.views.user_login, name='login'),
    path('',accountsapp.views.home,name='home'),
    path('articles/', accountsapp.views.articles_list, name='articles_list'),
    path('article/<int:article_id>/',accountsapp.views.read_Article,name='read_article'),
    path('facilities/', accountsapp.views.view_facilities, name='view_facilities_list'),
    path('view_facility/<int:facility_id>/',accountsapp.views.view_facility_detail,name='view_facility_detail'),
    path('doctors/',accountsapp.views.view_doctors,name='doctors_list'),
    path('dashboard/',accountsapp.views.dashboard_redirect,name='dashboard_redirect')
]
