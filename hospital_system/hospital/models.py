from django.db import models
from shortuuid.django_fields import ShortUUIDField
import datetime
# Create your models here.
class Patient(models.Model):
    patient_name = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    patient_token = ShortUUIDField(length=11, unique=True)
    address = models.CharField(max_length=30)
    mobile = models.CharField(max_length=20,null=True)
    medical_history = models.CharField(max_length=300)
    def __str__(self):
        return "ID: " + str(self.id) + " | Patient Name: " + str(self.patient_name)

departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]
class Doctor(models.Model):
    doctor_name = models.CharField(max_length=40)
    password = models.CharField(max_length=40)
    doctor_token = ShortUUIDField(length=11, unique=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    available = models.BooleanField(default=False)
    def __str__(self):
        return "ID: " + str(self.id) + " | Doctor Name: " + str(self.doctor_name)

class Appointment(models.Model):
    patient_name=models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_name=models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointmentDate=models.DateField()
    symptoms=models.TextField(max_length=500)
    

