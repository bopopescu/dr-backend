from datetime import datetime, date
from dateutil import parser
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from oauth2_provider.models import AccessToken
from django.utils import timezone

from .serializers import PatientSerializer, TreatmentListSerializer, AppointmentSerializer, AccountSerializer,TreatmentsSerializer, TreatmentFilesSerializer
import datetime
from users.models import User
from api.models import  Patient, TreatmentList, Appointment, Account, Treatments, TreatmentFiles
from users.serializers import UserSerializer
from django.db.models import Avg
import json
from .utilities import getmealType
import os
import requests


os.environ['TZ'] = 'Asia/Kolkata'
# from django.db.models import F
# Create your views here.l
isMeal, get_meal_type = getmealType()

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@login_required()
def patient_view(request, **kwargs):
    dt = datetime.datetime.now()
    dateToday = datetime.date.today()
    dt = dt.replace(minute=0, second=0, microsecond=0)


    if request.method == 'GET':
        pateint_details=Patient.objects.filter(doctor_treated=request.user)
        patientSerializer = PatientSerializer(pateint_details, many=True)
        return Response(status=200, data=patientSerializer.data)

    elif request.method =='PUT':
        pateint_details=Patient.objects.filter(doctor_treated=request.user, patient_key=request.data['patient_key']).update(**request.data)
        return Response(status=200, data={"response":"data updated sucessfully"})


    elif request.method =='DELETE':
        patient_key=request.data['pk']
        patient_details=Patient.objects.filter(patient_key=patient_key)
        patient_details.delete()
        return Response(status=200, data={"response":"pateint is sucessfully deleted"})


    elif request.method == 'POST':
        user_details=User.objects.filter(email=request.user)
        userSerializer = UserSerializer(user_details, many=True)
        if Patient.objects.filter(phone=request.data['phone']) or  Patient.objects.filter(email=request.data['email']):
            return Response(status=400, data={'error': 'This user phone or email already exists'})
        else:
            if userSerializer.data[0]['is_admin']:
                patient = Patient.objects.create(
                        email=request.data['email'],
                        user_name=request.data['user_name'],
                        sex=request.data['sex'],
                        age=request.data['age'],
                        phone=request.data['phone'],
                        medical_history=request.data['medical_history'],
                        address=request.data['address'],
                        doctor_treated=request.user,
                        created = dateToday,
                    )

                patientSerializer = PatientSerializer(instance=patient)
                if request.data['phone']:
                    # msg = requests.get('http://198.24.149.4/API/pushsms.aspx?loginID=drtangri&password=abc123&mobile='+str(request.data['phone'])+'&text=Hello you are added to dr tangri clinic&senderid=DEMOOO&route_id=7&Unicode=0')
                    # print msg.MsgStatus
                    # print msg
                    # print msg.status
                    return Response(status=200, data={"response":"patient added sucessfully"})
    else:
        return Response(status=400, data={"error":"permission denied"})



@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@login_required()
def patientfilter_view(request, **kwargs):
    dt = datetime.datetime.now()
    dateToday = datetime.date.today()
    dt = dt.replace(minute=0, second=0, microsecond=0)


    if request.method == 'POST':
        user_details=User.objects.filter(email=request.user)
        userSerializer = UserSerializer(user_details, many=True)
        patient_filter = Patient.objects.filter(phone__icontains=request.data['qphone'], user_name__icontains=request.data['qname'])

        patient_data = PatientSerializer(patient_filter, many=True)
        return Response(status=200, data=patient_data.data)




@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@login_required()
def treatmentlist_view(request, **kwargs):
    dt = datetime.datetime.now()
    dateToday = datetime.date.today()
    dt = dt.replace(minute=0, second=0, microsecond=0)


    if request.method == 'GET':
        pateint_details=TreatmentList.objects.filter()
        treatmentSerializer = TreatmentListSerializer(pateint_details, many=True)
        return Response(status=200, data=treatmentSerializer.data)


    elif request.method =='DELETE':
        treatment_key=request.data['pk']
        treatment_details=TreatmentList.objects.filter(treatment_key=treatment_key)
        treatment_details.delete()
        return Response(status=200, data={"response":"treatment type is sucessfully deleted"})


    elif request.method =='PUT':
        pateint_details=TreatmentList.objects.filter(treatment_key=request.data['treatment_key']).update(**request.data)
        return Response(status=200, data={"response":"data updated sucessfully"})

    elif request.method == 'POST':
        user_details=User.objects.filter(email=request.user)
        if TreatmentList.objects.filter(description=request.data['description']):
            return Response(status=400, data={'error': 'This type already exists'})

        # print patientSerializer
        print request.user
        userSerializer = UserSerializer(user_details, many=True)
        if userSerializer.data[0]['is_admin']:
            treatment = TreatmentList.objects.create(

                    description=request.data['description'],

                )

            treatmentSerializer = TreatmentListSerializer(instance=treatment)

            return Response(status=200, data={"response":"treatment added sucessfully"})
        else:
            return Response(status=400, data={"error":"permission denied"})


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@login_required()
def appointment_view(request, **kwargs):
    dt = datetime.datetime.now()
    dateToday = datetime.date.today()
    dt = dt.replace(minute=0, second=0, microsecond=0)


    if request.method == 'GET':
        appointment_details=Appointment.objects.filter(treatment__doctor=request.user)
        appointmentSerializer = AppointmentSerializer(appointment_details, many=True)
        return Response(status=200, data=appointmentSerializer.data)

    elif request.method =='PUT':
        pateint_details=Appointment.objects.filter(treatment__doctor=request.user, appointment_key=request.data['appointment_key']).update(**request.data)
        return Response(status=200, data={"response":"data updated sucessfully"})

    elif request.method =='DELETE':
        appointment_key=request.data['pk']
        appointment_details=Appointment.objects.filter(appointment_key=appointment_key)
        appointment_details.delete()
        return Response(status=200, data={"response":"Appointment is sucessfully deleted"})

    elif request.method == 'POST':
        user_details=User.objects.filter(email=request.user)
        userSerializer = UserSerializer(user_details, many=True)
        treatment_details=Treatments.objects.get(treatments_key=request.data['treatments_key'])
        if userSerializer.data[0]['is_admin']:
            appointment = Appointment.objects.create(
                    appointment_time=request.data['appointment_time'],
                    created = dateToday,
                    treatment=treatment_details

                )
            patientSerializer = PatientSerializer(instance=appointment)

            return Response(status=200, data={"response":"appointment added sucessfully"})
        else:
            return Response(status=400, data={"error":"permission denied"})


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@login_required()
def appointmentfilter_view(request, **kwargs):
    dt = datetime.datetime.now()
    dateToday = datetime.date.today()
    dt = dt.replace(minute=0, second=0, microsecond=0)


    if request.method == 'POST':
        user_details=User.objects.filter(email=request.user)
        userSerializer = UserSerializer(user_details, many=True)
        appointment_details=Appointment.objects.filter(appointment_time__date=request.data['qtime'])
        print request.data['qtime']
        appoint_serial = AppointmentSerializer(appointment_details, many=True)
        print appoint_serial.data[0]['appointment_time']
        return Response(status=200, data=appoint_serial.data)





# @api_view(['POST', 'GET', 'PUT', 'DELETE'])
# @login_required()
# def account_view(request, **kwargs):
#     dt = datetime.datetime.now()
#     dateToday = datetime.date.today()
#     dt = dt.replace(minute=0, second=0, microsecond=0)
#
#
#     if request.method == 'GET':
#         account_details=Account.objects.filter(doctor=request.user)
#         aaccountSerializer = AccountSerializer(account_details, many=True)
#         return Response(status=200, data=aaccountSerializer.data)
#
#     elif request.method == 'POST':
#         user_details=User.objects.filter(email=request.user)
#         userSerializer = UserSerializer(user_details, many=True)
#         patient_details=Patient.objects.get(patient_key=request.data['patient_key'])
#         treatment_details=TreatmentList.objects.get(treatment_key=request.data['treatment_key'])
#         if userSerializer.data[0]['is_admin']:
#             account = Account.objects.create(
#                     invoice_no="invoice_no1",
#                     description=request.data['description'],
#                     teeth=request.data['teeth'],
#                     total_cost=request.data['total_cost'],
#                     net_cost="100",
#                     discount=request.data['discount'],
#                     doctor=request.user,
#                     created = dateToday,
#                     patient=patient_details,
#                     treatment=treatment_details
#
#                 )
#             accountSerializer = AccountSerializer(instance=account)
#
#             return Response(status=200, data={"response":"account added sucessfully"})
#         else:
#             return Response(status=400, data={"error":"permission denied"})

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@login_required()
def account_view(request, **kwargs):
    dt = datetime.datetime.now()
    dateToday = datetime.date.today()
    dt = dt.replace(minute=0, second=0, microsecond=0)


    if request.method == 'GET':
        account_details=Account.objects.filter(appointment__treatment__doctor=request.user)
        accountSerializer = AccountSerializer(account_details, many=True)
        responseData = accountSerializer.data
        return Response(status=200, data=responseData)


    elif request.method =='DELETE':
        account_key=request.data['pk']
        account_details=Account.objects.filter(account_key=account_key)
        account_details.delete()
        return Response(status=200, data={"response":"account  is sucessfully deleted"})

    elif request.method =='PUT':
        account_details=Account.objects.filter(account_key=request.data['account_key']).update(**request.data)
        account=Account.objects.get(account_key=request.data['account_key'])
        account.net_cost = float(request.data['total_cost']) - float(request.data['total_cost'])*float(request.data['discount'])*0.01
        account.save()


        return Response(status=200, data={"response":"data updated sucessfully"})

    elif request.method == 'POST':
        user_details=User.objects.filter(email=request.user)
        userSerializer = UserSerializer(user_details, many=True)
        # patient_details=Patient.objects.get(patient_key=request.data['patient_key'])
        # treatment_details=TreatmentList.objects.get(treatment_key=request.data['treatment_key'])
        appointment_details=Appointment.objects.get(appointment_key=request.data['appointment_key'])

        account_count = Account.objects.filter().count()
        if account_count==0:
            inv_key=0
        else:
            latest_acc_key = AccountSerializer(Account.objects.latest('account_key')).data['account_key']
            inv_key = latest_acc_key+1



        if Account.objects.filter(total_cost=request.data['total_cost'], appointment=appointment_details, discount=request.data['discount'], teeth=request.data['teeth'],created = dateToday):
            return Response(status=400, data={'error': 'This bill already exists for today'})
        if userSerializer.data[0]['is_admin']:

            net_cost = float(request.data['total_cost']) - float(request.data['total_cost'])*float(request.data['discount'])*0.01
            account = Account.objects.create(
                    invoice_no="INVTC0"+str(inv_key),
                    # description=request.data['description'],
                    teeth=request.data['teeth'],
                    total_cost=request.data['total_cost'],
                    net_cost=net_cost,
                    discount=request.data['discount'],
                    created = dateToday,
                    appointment=appointment_details,


                )
            accountSerializer = AccountSerializer(instance=account)

            return Response(status=200, data={"response":"account added sucessfully"})
        else:
            return Response(status=400, data={"error":"permission denied"})


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@login_required()
def invoice_view(request, **kwargs):
    dt = datetime.datetime.now()
    dateToday = datetime.date.today()
    dt = dt.replace(minute=0, second=0, microsecond=0)

    if request.method == 'POST':
        user_details=User.objects.filter(email=request.user)
        userSerializer = UserSerializer(user_details, many=True)

        if userSerializer.data[0]['is_admin']:
            account_key = request.data['account_key']
            account_details = Account.objects.filter(account_key=account_key)
            account_serail = AccountSerializer(account_details, many=True)

            return Response(status=200, data=account_serail.data)
        else:
            return Response(status=401, data={"error":"permission denied"})





@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@login_required()
def treatment_view(request, **kwargs):
    dt = datetime.datetime.now()
    dateToday = datetime.date.today()
    dt = dt.replace(minute=0, second=0, microsecond=0)


    if request.method == 'GET':
        account_details=Treatments.objects.filter(doctor=request.user)
        treatSerializer = TreatmentsSerializer(account_details, many=True)
        return Response(status=200, data=treatSerializer.data)

    elif request.method =='PUT':
        treatment_details=Account.objects.filter(treatments_key=request.data['treatments_key']).update(**request.data)
        treatment.save()
        return Response(status=200, data={"response":"data updated sucessfully"})

    elif request.method =='DELETE':
        treatments_key=request.data['pk']
        treat_details=Treatments.objects.filter(treatments_key=treatments_key)
        treat_details.delete()
        return Response(status=200, data={"response":"Treatment  is sucessfully deleted"})

    elif request.method == 'POST':
        user_details=User.objects.filter(email=request.user)
        userSerializer = UserSerializer(user_details, many=True)
        patient_details=Patient.objects.get(patient_key=request.data['patient_key'])
        treatment_type_details=TreatmentList.objects.get(treatment_key=request.data['treatment_key'])
        if userSerializer.data[0]['is_admin']:
            treat = Treatments.objects.create(
                    status=request.data['status'],
                    treatment_type=treatment_type_details,
                    doctor=request.user,
                    created = dateToday,
                    patient=patient_details,
                    # treatment=treatment_details,

                )
            treatmentsSerializer = TreatmentsSerializer(instance=treat)

            return Response(status=200, data={"response":"treatment added sucessfully"})
        else:
            return Response(status=400, data={"error":"permission denied"})


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@login_required()
def treatment_file_view(request, **kwargs):
    dt = datetime.datetime.now()
    dateToday = datetime.date.today()
    dt = dt.replace(minute=0, second=0, microsecond=0)

    print "------------0"

    if request.method == 'GET':
        account_details=TreatmentFiles.objects.filter(treatment__doctor=request.user)
        treatSerializer = TreatmentFilesSerializer(account_details, many=True)
        return Response(status=200, data=treatSerializer.data)


    elif request.method =='PUT':
        treatments_key=request.data['treatments_key']
        files_details=TreatmentFiles.objects.filter(treatment__treatments_key=treatments_key).update(**request.data)
        files_details.save()

    elif request.method =='DELETE':
        treatments_key=request.data['pk']
        files_details=TreatmentFiles.objects.filter(file_key=treatments_key)
        files_details.delete()
        return Response(status=200, data={"response":"file is sucessfully deleted"})

    elif request.method == 'POST':

        treatments_key=request.data['treatments_key']
        file_description=request.data['file_description']
        print file_description

        treatment_details=Treatments.objects.get(treatments_key=treatments_key)
        user_details=User.objects.filter(email=request.user)
        if TreatmentFiles.objects.filter(treatment__treatments_key=treatments_key,file_description=file_description):
            return Response(status=401, data={"error":"file with this data already exists"})

        userSerializer = UserSerializer(user_details, many=True)
        if userSerializer.data[0]['is_admin']:
            treatfile = TreatmentFiles.objects.create()
            treatfile.file_description=file_description
            treatfile.treatment=treatment_details
            treatfile.created = dateToday

            treatfile.files=request.data['file']

            treatfile.save()


    # treatmentsfileSerializer = TreatmentFilesSerializer(instance=treatfile)

            return Response(status=200, data={"response":"treatment file added sucessfully"})
        else:
            return Response(status=400, data={"error":"permission denied"})
