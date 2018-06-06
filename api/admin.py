from django.contrib import admin
from django.conf import settings
from django.http import HttpResponseRedirect
from django.conf.urls import include, url
from django.contrib.admin.views.decorators import staff_member_required

from .models import Patient, Appointment, TreatmentList, Account, Treatments, TreatmentFiles, InvoiceItem

# Register your models here.
class PateintAdmin(admin.ModelAdmin):
    list_display =('pk', 'patient_key','user_name', 'email', 'sex','age','phone','medical_history','address','doctor_treated')
    # list_filter = ('meal_type')
    search_fields = ['email']

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_key', 'appointment_time','treatment')
    # list_filter = ('meal_type')
    search_fields = ['patient']

class TreatmentListAdmin(admin.ModelAdmin):
    list_display = ('pk', 'description','treatment_key')
    # list_filter = ('meal_type')
    # search_fields = ['patient']

class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_key', 'appointment', 'invoice_no','teeth','discount')
    # list_filter = ('meal_type')
    # search_fields = ['patient']

class TreatmentsAdmin(admin.ModelAdmin):
    list_display = ('treatments_key','patient', 'treatment_type','doctor','status','created')
    # list_filter = ('meal_type')
    # search_fields = ['patient']

class TreatmentFilesAdmin(admin.ModelAdmin):
    list_display = ('file_key','files', 'treatment','file_description')
    # list_filter = ('meal_type')
    # search_fields = ['patient']

class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice','description', 'unit_price','quantity')

    # list_filter = ('meal_type')
    # search_fields = ['patient']


admin.site.register(Patient, PateintAdmin)
admin.site.register(TreatmentList, TreatmentListAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Treatments, TreatmentsAdmin)
admin.site.register(TreatmentFiles, TreatmentFilesAdmin)
admin.site.register(InvoiceItem, InvoiceItemAdmin)
