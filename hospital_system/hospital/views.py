from pickle import FALSE
from django.forms import PasswordInput
from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework.authtoken.views import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@api_view(['POST']) 
def register(request):   
    if request.method == 'POST':
        try:
            patient_name = request.data['patient_name']
        except KeyError:
            return Response({'Error': 'patient_name not provided'}, status=status.HTTP_400_BAD_REQUEST) 
        
        try:
            password = request.data['password']
        except KeyError:
            return Response({'Error': 'patient_name not provided'}, status=status.HTTP_400_BAD_REQUEST) 
        
        try:
            address = request.data['address']
        except KeyError:
            return Response({'Error': 'address not provided'}, status=status.HTTP_400_BAD_REQUEST)  
        
        try:
            mobile = request.data['mobile']
        except KeyError:
            return Response({'Error': 'mobileno not provided'}, status=status.HTTP_400_BAD_REQUEST)  
        
        try:
            medical_history = request.data['medical_history']
        except KeyError:
            return Response({'Error': 'medical_history not provided'}, status=status.HTTP_400_BAD_REQUEST)  
        
        link = Patient.objects.create(patient_name=patient_name,password=password,address=address,mobile=mobile,medical_history=medical_history)
        serializer =PatientSerializer(link)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    return Response(serializer.error, status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
def patient_login(request):
    if request.method == 'POST':
        try:
            patient_name = request.data['patient_name']
        except KeyError:
            return Response({'Error': 'patient_name not provided'}, status=status.HTTP_400_BAD_REQUEST) 
        
        try:
            password = request.data['password']
        except KeyError:
            return Response({'Error': 'patient_name not provided'}, status=status.HTTP_400_BAD_REQUEST) 
        
        try:
            patient = Patient.objects.get(patient_name=patient_name, password=password)
            if patient:
                return Response({'Token': patient.patient_token}, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
           return Response({'Error': "Invalid username or password."}, status=status.HTTP_204_NO_CONTENT)
    return Response({'Error': "something went wrong."}, status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET'])
def doctor_login(request,doctor_name,password):
    if request.method == 'GET':
        # try:
        #     doctor_name = request.data['doctor_name']
        # except KeyError:
        #     return Response({'Error': 'doctor_name not provided'}, status=status.HTTP_400_BAD_REQUEST) 
        
        # try:
        #     password = request.data['password']
        # except KeyError:
        #     return Response({'Error': 'patient_name not provided'}, status=status.HTTP_400_BAD_REQUEST) 
        
        try:
            doctor = Doctor.objects.get(doctor_name=doctor_name, password=password)
            if doctor:
                return Response({'Token': doctor.doctor_token}, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
           return Response({'Error': "Invalid username or password."}, status=status.HTTP_204_NO_CONTENT)
    return Response({'Error': "something went wrong."}, status=status.HTTP_204_NO_CONTENT)

    
@api_view(['GET']) 
def logout(request):
    auth_logout(request)
    data = {'Success': 'Sucessfully logged out'}
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def patient_profile(request,pk): 
    if request.method == 'GET':
        try:
            patient = Patient.objects.get(id=pk)
            patient_serializer = PatientSerializer(patient)
            return Response(patient_serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "Somthing went wrong!"}, status=status.HTTP_403_FORBIDDEN)  

@api_view(['GET'])
def doctor_profile(request,pk): 
    if request.method == 'GET':
        try:
            doctor = Doctor.objects.get(id=pk)
            doctor_serializer = DoctorSerializer(doctor)
            return Response(doctor_serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "Somthing went wrong!"}, status=status.HTTP_403_FORBIDDEN) 


@api_view(['POST']) 
def add_appointment(request):   
        if request.method == 'POST':
        
            try:
                user = request.data['patient_name']
            except KeyError:
                return Response({'Error': 'patient_name not provided'}, status=status.HTTP_400_BAD_REQUEST) 

            try:
                user1 = request.data['doctor_name']
            except KeyError:
                return Response({'Error': 'doctor_name not provided'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                appointment_date = request.data['appointmentDate']
            except KeyError:
                return Response({'Error': 'appointmentDate not provided'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                symptoms = request.data['symptoms']
            except KeyError:
                return Response({'Error': 'symptoms not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
            try:
                user_qry = Patient.objects.get(patient_name=user)
            except Patient.DoesNotExist:
                return Response({'Error': 'Invalid provided data of patientname'}, status=status.HTTP_400_BAD_REQUEST)
    
            try:
                user_qry1 = Doctor.objects.get(doctor_name=user1)
            except Doctor.DoesNotExist:
                return Response({'Error': 'Invalid provided data of doctorname'}, status=status.HTTP_400_BAD_REQUEST)
        

        doctor =Doctor.objects.filter(doctor_name=user1,available=True)
        print("----",doctor)
        if doctor:
            link =  Appointment.objects.create(patient_name=user_qry,doctor_name=user_qry1,appointmentDate=appointment_date,symptoms=symptoms)
            serializer =AppointmentSerializer(link)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"Error": "doctor is not available!"}, status=status.HTTP_403_FORBIDDEN) 

@api_view(['GET'])
def appointment_details(request,token): 
    if request.method == 'GET':
        doctor = Doctor.objects.get(doctor_token=token)
        try:
            appointment = Appointment.objects.filter(doctor_name=doctor)
            appointment_serializer = AppointmentSerializer(appointment,many = True)
            return Response(appointment_serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "Somthing went wrong!"}, status=status.HTTP_403_FORBIDDEN) 

@api_view(['GET'])
def appointment(request,token): 
    if request.method == 'GET':
        patient = Patient.objects.get(patient_token=token)
        try:
            appointment = Appointment.objects.filter(patient_name=patient)
            appointment_serializer = AppointmentSerializer(appointment,many = True)
            return Response(appointment_serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "Somthing went wrong!"}, status=status.HTTP_403_FORBIDDEN) 

@api_view(['GET'])
def listing(request,pk): 
    if request.method == 'GET':
        try:
            services = Doctor.objects.get(id=pk)
            service_serializer = DoctorSerializer(services)
            return Response(service_serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "Somthing went wrong!"}, status=status.HTTP_403_FORBIDDEN) 