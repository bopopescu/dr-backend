from datetime import datetime, date
from dateutil import parser
import dateutil.parser
import urllib
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from oauth2_provider.models import AccessToken
from django.utils import timezone

from .serializers import PatientSerializer, TreatmentListSerializer, AppointmentSerializer, AccountSerializer,TreatmentsSerializer, TreatmentFilesSerializer, InvoiceItemSerializer, BillSerializer
import datetime
from users.models import User
from api.models import  Patient, TreatmentList, Appointment, Account, Treatments, TreatmentFiles, InvoiceItem, Bill
from users.serializers import UserSerializer
from django.db.models import Avg
import json
from .utilities import getmealType
import os
import requests
from .sendmessage import sendSMSLocal
from decimal import Decimal


os.environ['TZ'] = 'Asia/Kolkata'
# from django.db.models import F
# Create your views here.l
isMeal, get_meal_type = getmealType()

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@login_required()
def user_details_view(request, **kwargs):
    if request.method == 'GET':
        user_details=User.objects.filter(email=request.user)
        user_serial = UserSerializer(user_details, many=True)
        return Response(status=200, data=user_serial.data)

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@login_required()
def patient_view(request, **kwargs):
    dt = datetime.datetime.now()
    dateToday = datetime.date.today()
    dt = dt.replace(minute=0, second=0, microsecond=0)


    if request.method == 'GET':
        pateint_details=Patient.objects.all()
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
        # if Patient.objects.filter(phone=request.data['phone']) or  Patient.objects.filter(email=request.data['email']):
        #     return Response(status=400, data={'error': 'This user phone or email already exists'})
        # else:
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
            new_id = str(patientSerializer.data['pk'])
            if request.data['phone']:
                msg_text="Welcome%20Mr%2FMs.%20"+request.data['user_name']+"%20%0AYou%20have%20been%20registered%20with%20patient%20ID%20%3A%20"+new_id+".%0A%0AStay%20Healthy!%0A%0ADr.%20Tangri%27s%20Dental%20Clinic%0A%2B91-981-028-9955"
                # resp =  sendSMSLocal('EQyiOW++/Kc-xigYQVVGFl5KOY96AQpzrnoiet8Qzl', str(request.data['phone']), 'TANGRI', msg_text)
                # print resp
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
def getuser_view(request, **kwargs):
    dt = datetime.datetime.now()
    dateToday = datetime.date.today()
    dt = dt.replace(minute=0, second=0, microsecond=0)


    if request.method == 'GET':
        user_details=User.objects.all()
        userSerializer = UserSerializer(user_details, many=True)

        return Response(status=200, data=userSerializer.data)




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
        appointment_details=Appointment.objects.all()
        appointmentSerializer = AppointmentSerializer(appointment_details, many=True)
        return Response(status=200, data=appointmentSerializer.data)

    elif request.method =='PUT':
        pateint_details=Appointment.objects.filter(treatment__doctor=request.user, appointment_key=request.data['appointment_key']).update(**request.data)
        return Response(status=200, data={"response":"data updated sucessfully"})

    elif request.method =='DELETE':
        appointment_key=request.data['pk']
        appointment_details=Appointment.objects.filter(appointment_key=appointment_key)
        patientSerializer=AppointmentSerializer(appointment_details, many=True)
        phone = patientSerializer.data[0]['patient_phone']
        name = patientSerializer.data[0]['patient_name']
        app_id = str(patientSerializer.data[0]['appointment_key'])
        date = patientSerializer.data[0]['appointment_time']
        dat = dateutil.parser.parse(date) + datetime.timedelta(minutes=330)
        final_date = urllib.quote(str(dat)[:10])
        final_time = urllib.quote(str(dat)[11:16])
        print final_time
        print final_date
        msg_txt="Mr%2FMs.%20"+name+"%20%2C%0AYour%20appointment%20has%20been%20cancelled%20for%20"+final_date+"%20at%20"+final_time+"%20.%0A%0AStay%20Healthy!%0A%0ADr.%20Tangri%27s%20Dental%20Clinic%0A%2B91-981-028-9955"
        resp =  sendSMSLocal('EQyiOW++/Kc-xigYQVVGFl5KOY96AQpzrnoiet8Qzl', phone, 'TANGRI', msg_txt)
        print resp
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
            patientSerializer = AppointmentSerializer(instance=appointment)
            phone = patientSerializer.data['patient_phone']
            name = patientSerializer.data['patient_name']
            app_id = str(patientSerializer.data['appointment_key'])
            date = patientSerializer.data['appointment_time']
            dat = dateutil.parser.parse(date) + datetime.timedelta(minutes=330)
            final_date = urllib.quote(str(dat)[:10])
            final_time = urllib.quote(str(dat)[11:16])
            print final_time
            print final_date

            msg_text="Mr%2FMs.%20"+name+"%20%2C%0AYour%20appointment%20has%20been%20booked%20for%20"+final_date+"%20at%20"+final_time+"%20.%0A%20%0AStay%20Healthy!%0A%20%0ADr.%20Tangri%27s%20Dental%20Clinic%0A%2B91-981-028-9955"
            resp =  sendSMSLocal('EQyiOW++/Kc-xigYQVVGFl5KOY96AQpzrnoiet8Qzl', phone, 'TANGRI', msg_text)
            print resp
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
        appointment_details=Appointment.objects.filter(appointment_time__contains=request.data['qtime'])
        print request.data['qtime']
        appoint_serial = AppointmentSerializer(appointment_details, many=True)
        return Response(status=200, data=appoint_serial.data)



@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@login_required()
def treatappointmentfilter_view(request, **kwargs):
    dt = datetime.datetime.now()
    dateToday = datetime.date.today()
    dt = dt.replace(minute=0, second=0, microsecond=0)


    if request.method == 'POST':
        user_details=User.objects.filter(email=request.user)
        userSerializer = UserSerializer(user_details, many=True)
        treat_details=Treatments.objects.filter(treatments_key=request.data['treatments_key'])
        treat_serial = TreatmentsSerializer(treat_details, many=True)
        appointment_details=Appointment.objects.filter(treatment=treat_details)
        appoint_serial = AppointmentSerializer(appointment_details, many=True)
        out = {}
        out['main'] = appoint_serial.data
        out['treatments_status'] = treat_serial.data[0]['status']
        print
        return Response(status=200, data=out)


    elif request.method =='PUT':
        treat_details=Treatments.objects.filter(treatments_key=request.data['treatments_key']).update(**request.data)
        return Response(status=200, data={"response":"data updated sucessfully"})

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@login_required()
def treatpatientfilter_view(request, **kwargs):
    dt = datetime.datetime.now()
    dateToday = datetime.date.today()
    dt = dt.replace(minute=0, second=0, microsecond=0)


    if request.method == 'POST':
        treat_details=Treatments.objects.filter(patient__pk=request.data['patient_key'])
        treat_serial = TreatmentsSerializer(treat_details, many=True)

        return Response(status=200, data=treat_serial.data)

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@login_required()
def appointmentmessage_view(request, **kwargs):
    dt = datetime.datetime.now()
    dateToday = datetime.date.today()

    if request.method == 'GET':
        users = User.objects.all()
        user_serial = UserSerializer(users, many=True)

        # print user_serial.data
        phones = []
        for x in range(len(user_serial.data)):
            phones.append(user_serial.data[x]['phone'])
        phones_len = len(phones)
        # print phones_len
        print dateToday

        for data in range(phones_len):
            appointment_details=Appointment.objects.filter(treatment__doctor__phone=phones[data], appointment_time__contains=dateToday)
            count=Appointment.objects.filter(treatment__doctor__phone=phones[data], appointment_time__contains=dateToday).count()
            doctor_details=User.objects.filter(phone=phones[data])
            doc_serial = UserSerializer(doctor_details, many=True)
            print doc_serial.data
            doc_name = doc_serial.data[0]['user_name']
            print "sent count msg... "+phones[data]+" "+str(count)
            msg_text="Good%20Morning%20Dr.%20"+doc_name+"%0A%0AYou%20have%20"+str(count)+"%20appointments%20scheduled%20for%20today."
            resp1 =  sendSMSLocal('EQyiOW++/Kc-xigYQVVGFl5KOY96AQpzrnoiet8Qzl', phones[data], 'TANGRI', msg_text)
            print resp1
            appoint_serial = AppointmentSerializer(appointment_details, many=True)
            var = count/3
            print var
            pair_msg=""
            if var>=1:
                for x in range(var):
                    name1 = appoint_serial.data[x*3]['patient_name']
                    time1 = appoint_serial.data[x*3]['appointment_time']
                    name2 = appoint_serial.data[(x*3)+1]['patient_name']
                    time2 = appoint_serial.data[(x*3)+1]['appointment_time']
                    name3 = appoint_serial.data[(x*3)+2]['patient_name']
                    time3 = appoint_serial.data[(x*3)+2]['appointment_time']

                    dat1 = dateutil.parser.parse(time1) + datetime.timedelta(minutes=330)
                    final_time1 = urllib.quote(str(dat1)[11:16])
                    dat2 = dateutil.parser.parse(time2) + datetime.timedelta(minutes=330)
                    final_time2 = urllib.quote(str(dat2)[11:16])
                    dat3 = dateutil.parser.parse(time3) + datetime.timedelta(minutes=330)
                    final_time3 = urllib.quote(str(dat3)[11:16])

                    msg_text3="Patient%3A%20"+name1+"%0ATime%3A%20"+final_time1+"%0APatient%3A%20"+name2+"%0ATime%3A%20"+final_time2+"%0APatient%3A%20"+name3+"%0ATime%3A%20"+final_time3

                    # msg_text3="Patient%3A%20XXXXXXXXXX%0ATime%3A%20XXX%0APatient%3A%20XXXXXXXXXX%0ATime%3A%20XXX%0APatient%3A%20XXXXXXXXXX%0ATime%3A%20XXX"

                    resp2 =  sendSMSLocal('EQyiOW++/Kc-xigYQVVGFl5KOY96AQpzrnoiet8Qzl', phones[data], 'TANGRI', msg_text3)
                    print resp2
                    print "send message 3 pair... "+str(x) +" "+str(final_time3)

            if (count%3==1):
                name1 = appoint_serial.data[-1]['patient_name']
                time1 = appoint_serial.data[-1]['appointment_time']
                dat1 = dateutil.parser.parse(time1) + datetime.timedelta(minutes=330)
                final_time1 = urllib.quote(str(dat1)[11:16])
                msg_text1="Patient%3A%20"+name1+"%0ATime%3A%20"+final_time1
                resp3 =  sendSMSLocal('EQyiOW++/Kc-xigYQVVGFl5KOY96AQpzrnoiet8Qzl', phones[data], 'TANGRI', msg_text1)
                print resp3
                print "send message 1"

            elif  (count%3==2):
                name1 = appoint_serial.data[-2]['patient_name']
                time1 = appoint_serial.data[-2]['appointment_time']
                name2 = appoint_serial.data[-1]['patient_name']
                time2 = appoint_serial.data[-1]['appointment_time']
                dat1 = dateutil.parser.parse(time1) + datetime.timedelta(minutes=330)
                final_time1 = urllib.quote(str(dat1)[11:16])
                dat2 = dateutil.parser.parse(time2) + datetime.timedelta(minutes=330)
                final_time2 = urllib.quote(str(dat2)[11:16])


                # msg_text2="Patient%3A%20"+name1+"%0ATime%3A%20"+final_time1+"%0APatient%3A%20"+name2+"%0ATime%3A%20"+final_time2
                msg_text2="Patient%3A%20"+name1+"%0ATime%3A%20"+final_time1+"%0APatient%3A%20"+name2+"%0ATime%3A%20"+final_time2
                # msg_text2="Patient%3A%20XXX%0ATime%3A%20XXXX%0APatient%3A%20XX%0ATime%3A%20XXX"
                resp4 =  sendSMSLocal('EQyiOW++/Kc-xigYQVVGFl5KOY96AQpzrnoiet8Qzl', phones[data], 'TANGRI', msg_text2)
                print resp4

                print "send message 2"

        return Response(status=200, data={"response":"sucessfully sent"})


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
        account_details=Account.objects.all()
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



        if Account.objects.filter(appointment=appointment_details, discount=request.data['discount'],created = dateToday):
            return Response(status=400, data={'error': 'This bill already exists for today'})
        if userSerializer.data[0]['is_admin']:


            account = Account.objects.create(
                    invoice_no="INVTC0"+str(inv_key),
                    # description=request.data['description'],
                    # teeth=request.data['teeth'],
                    discount=request.data['discount'],
                    created = dateToday,
                    appointment=appointment_details,


                )

            invoiceitems = request.data['invoiceitems']
            accountSerializer = AccountSerializer(instance=account)
            new_account_id=accountSerializer.data['account_key']
            account_details=Account.objects.get(account_key=accountSerializer.data['account_key'])
            for x in range(len(invoiceitems)):
                invoice = InvoiceItem.objects.create(
                            invoice=account_details,
                            description=invoiceitems[x]['item'],
                            unit_price=Decimal(invoiceitems[x]['price']),
                            quantity=Decimal(invoiceitems[x]['qty'])
                )
                print invoice
                invoiceserial = InvoiceItemSerializer(instance=invoice)



            return Response(status=200, data={"response":"account added sucessfully","account_key":new_account_id})
        else:
            return Response(status=400, data={"error":"permission denied"})

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@login_required()
def bill_invoice_view(request, **kwargs):
    dt = datetime.datetime.now()
    dateToday = datetime.date.today()
    dt = dt.replace(minute=0, second=0, microsecond=0)


    if request.method == 'POST':
        estimate_details = Account.objects.get(account_key=request.data['estimate'])
        bill_details=Bill.objects.filter(estimate=estimate_details)
        billSerializer = BillSerializer(bill_details, many=True)
        responseData = billSerializer.data
        return Response(status=200, data=responseData)

@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@login_required()
def bill_view(request, **kwargs):
    dt = datetime.datetime.now()
    dateToday = datetime.date.today()
    dt = dt.replace(minute=0, second=0, microsecond=0)


    if request.method == 'POST':
        estimate_details = Account.objects.get(account_key=request.data['estimate'])
        if Bill.objects.filter(estimate=estimate_details):
            return Response(status=400, data={'error': 'This estimate is already billed'})
        bill_details=Bill.objects.create(estimate=estimate_details)
        billSerializer = BillSerializer(instance=bill_details)
        estimate_details.is_bill=True
        estimate_details.save()
        responseData = billSerializer.data
        return Response(status=200, data=responseData)



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
            item_details = InvoiceItem.objects.filter(invoice=account_details)
            account_serial = AccountSerializer(account_details, many=True)
            items_serial = InvoiceItemSerializer(item_details, many=True)
            bro = {}
            bro['inovice_main'] = account_serial.data
            bro['inovice_items'] = items_serial.data
            bro['total'] = Account.objects.get(account_key=account_key).total()

            return Response(status=200, data=bro)
        else:
            return Response(status=401, data={"error":"permission denied"})


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@login_required()
def appointment_estimate_filter_view(request, **kwargs):
    dt = datetime.datetime.now()
    dateToday = datetime.date.today()
    dt = dt.replace(minute=0, second=0, microsecond=0)

    if request.method == 'POST':

        app_details = Appointment.objects.get(appointment_key=request.data['appointment_key'])
        estimate_details = Account.objects.filter(appointment=app_details)
        est_serial = AccountSerializer(estimate_details, many=True)

        return Response(status=200, data=est_serial.data)





@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@login_required()
def treatment_view(request, **kwargs):
    dt = datetime.datetime.now()
    dateToday = datetime.date.today()
    dt = dt.replace(minute=0, second=0, microsecond=0)


    if request.method == 'GET':
        account_details=Treatments.objects.all()
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
        doctor_details = User.objects.get(email=request.data['dr_email'])
        user_details=User.objects.filter(email=request.user)
        userSerializer = UserSerializer(user_details, many=True)
        patient_details=Patient.objects.get(patient_key=request.data['patient_key'])
        treatment_type_details=TreatmentList.objects.get(treatment_key=request.data['treatment_key'])
        if userSerializer.data[0]['is_admin']:
            treat = Treatments.objects.create(
                    status=request.data['status'],
                    treatment_type=treatment_type_details,
                    doctor=doctor_details,
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
        account_details=TreatmentFiles.objects.all()
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


@api_view(['POST', 'GET', 'PUT', 'DELETE'])
@login_required()
def treatment_file_filter_view(request, **kwargs):
    dt = datetime.datetime.now()
    dateToday = datetime.date.today()
    dt = dt.replace(minute=0, second=0, microsecond=0)

    print "------------0"


    if request.method == 'POST':

        treatments_key=request.data['treatments_key']

        treatfiles = TreatmentFiles.objects.filter(treatment__treatments_key=treatments_key)

        file_serial = TreatmentFilesSerializer(treatfiles, many=True)

        return Response(status=200, data=file_serial.data)
