from rest_framework import serializers

from .models import Patient, Appointment, TreatmentList, Account, Treatments, TreatmentFiles, InvoiceItem, Bill
from users.serializers import UserSerializer
import datetime

from django.db.models import Avg

class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = ('pk', 'user_name', 'email', 'sex','age','phone','medical_history','address','doctor_treated')

class TreatmentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = TreatmentList
        fields = ('pk', 'description','treatment_key')

class AppointmentSerializer(serializers.ModelSerializer):

    doctor_name = serializers.ReadOnlyField(source='treatment.doctor.user_name', read_only=True)
    patient_name = serializers.ReadOnlyField(source='treatment.patient.user_name', read_only=True)
    patient_id = serializers.ReadOnlyField(source='treatment.patient.pk', read_only=True)
    patient_phone = serializers.ReadOnlyField(source='treatment.patient.phone', read_only=True)
    # treatment_type = serializers.ReadOnlyField(source='treatment.description', read_only=True)

    class Meta:
        model = Appointment
        fields = ('appointment_key', 'appointment_time','treatment','doctor_name','patient_name', 'patient_id','patient_phone')

class AccountSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='appointment.treatment.patient.user_name', read_only=True)
    patient_id = serializers.ReadOnlyField(source='appointment.treatment.patient.pk', read_only=True)
    patient_age = serializers.ReadOnlyField(source='appointment.treatment.patient.age', read_only=True)
    patient_sex = serializers.ReadOnlyField(source='appointment.treatment.patient.sex', read_only=True)
    patient_contact = serializers.ReadOnlyField(source='appointment.treatment.patient.phone', read_only=True)
    patient_address = serializers.ReadOnlyField(source='appointment.treatment.patient.address', read_only=True)
    appointment_time = serializers.ReadOnlyField(source='appointment.appointment_time', read_only=True)
    doctor_name = serializers.ReadOnlyField(source='appointment.treatment.doctor.user_name', read_only=True)
    treatment_key = serializers.ReadOnlyField(source='appointment.treatment.pk', read_only=True)

    class Meta:
        model = Account
        fields = ('account_key', 'appointment', 'invoice_no','teeth','discount','patient_name','patient_age','patient_contact','patient_address','appointment_time','doctor_name','patient_id','patient_sex','is_bill','treatment_key')

class TreatmentsSerializer(serializers.ModelSerializer):

    doctor_name = serializers.ReadOnlyField(source='doctor.user_name', read_only=True)
    patient_name = serializers.ReadOnlyField(source='patient.user_name', read_only=True)
    treatment_type_name = serializers.ReadOnlyField(source='treatment_type.description', read_only=True)

    class Meta:
        model = Treatments
        fields = ('treatments_key','patient', 'treatment_type','doctor','status','created','doctor_name','patient_name','treatment_type_name')

class TreatmentFilesSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='treatment.patient.user_name', read_only=True)

    class Meta:
        model = TreatmentFiles
        fields = ('file_key','files', 'treatment','file_description','patient_name')

class InvoiceItemSerializer(serializers.ModelSerializer):

    # print serializers.ReadOnlyField(source='invoice', read_only=True)
    class Meta:
        model = InvoiceItem
        fields = ('pk','invoice','description', 'unit_price','quantity')

class BillSerializer(serializers.ModelSerializer):

    # print serializers.ReadOnlyField(source='invoice', read_only=True)
    class Meta:
        model = Bill
        fields = ('bill_key','estimate')
