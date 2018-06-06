from rest_framework import serializers

from .models import Patient, Appointment, TreatmentList, Account, Treatments, TreatmentFiles
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
    # treatment_type = serializers.ReadOnlyField(source='treatment.description', read_only=True)

    class Meta:
        model = Appointment
        fields = ('appointment_key', 'appointment_time','treatment','doctor_name','patient_name')

class AccountSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='appointment.treatment.patient.user_name', read_only=True)

    class Meta:
        model = Account
        fields = ('account_key', 'appointment', 'invoice_no','teeth','discount','patient_name')

class TreatmentsSerializer(serializers.ModelSerializer):

    doctor_name = serializers.ReadOnlyField(source='doctor.user_name', read_only=True)
    patient_name = serializers.ReadOnlyField(source='patient.user_name', read_only=True)

    class Meta:
        model = Treatments
        fields = ('treatments_key','patient', 'treatment_type','doctor','status','created','doctor_name','patient_name')

class TreatmentFilesSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='treatment.patient.user_name', read_only=True)

    class Meta:
        model = TreatmentFiles
        fields = ('file_key','files', 'treatment','file_description','patient_name')
