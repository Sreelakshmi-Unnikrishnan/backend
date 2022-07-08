from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views

urlpatterns = [
    path('login/patient/', views.patient_login, name='patientlogin'),
    path('login/doctor/<str:doctor_name>/<str:password>/', views.doctor_login, name='doctorlogin'),
    path('logout/', views.logout, name='logout'),
    path('patient_profile/<int:pk>/', views.patient_profile, name='patient_profile'),
    path('doctor_profile/<int:pk>/', views.doctor_profile, name='doctor_profile'),
    path('register/patient/', views.register, name='register_patient'),
    path('add_appointment/', views.add_appointment, name='add_appointment'),
    path('appointment_details/<str:token>/', views.appointment_details, name='appointment_details'),
    path('appointment/<str:token>/', views.appointment, name='appointment_details'),
    path('listing/<int:pk>/', views.listing, name='doctor'),
]