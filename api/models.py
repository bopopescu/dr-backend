from __future__ import unicode_literals
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from users.models import User
from decimal import Decimal



class Patient(models.Model):
    patient_key = models.AutoField(primary_key=True)
    email = models.EmailField(verbose_name='email', max_length=255, unique=True,null=True)
    user_name = models.CharField(max_length=30, blank=True)
    sex = models.CharField(max_length=30, blank=True)
    age = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    medical_history = models.CharField(max_length=300, blank=True)
    address = models.CharField(max_length=300, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    avatar = models.FileField(upload_to='avatars/', null=True, blank=True)
    doctor_treated = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created = models.DateField(null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return (self.email)

    class Meta:
        verbose_name_plural = 'Patient'


class TreatmentList(models.Model):
    treatment_key = models.AutoField(primary_key=True)
    description = models.CharField(max_length=500, blank=True)


    def __str__(self):
        return (str(self.treatment_key))

    class Meta:
        verbose_name_plural = 'Treatments List'







class Treatments(models.Model):
    treatments_key = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, null=True, on_delete=models.CASCADE)
    treatment_type = models.ForeignKey(TreatmentList, null=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created = models.DateField(null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return (str(self.treatments_key))


    class Meta:
        verbose_name_plural = 'Treatments'


class Appointment(models.Model):
    appointment_key = models.AutoField(primary_key=True)
    appointment_time = models.DateTimeField( null=True, blank=True)
    treatment = models.ForeignKey(Treatments, null=True, on_delete=models.CASCADE)
    created = models.DateField(null=True)
    updated = models.DateTimeField(null=True)

    def __str__(self):
        return (str(self.appointment_key))


    class Meta:
        verbose_name_plural = 'Appointments'



def get_upload_to(instance, filename):
    return 'upload/%d/%s' % (instance.treatment.treatments_key, filename)

class TreatmentFiles(models.Model):
    file_key = models.AutoField(primary_key=True)
    files = models.FileField(upload_to=get_upload_to, null=True, blank=True)
    treatment = models.ForeignKey(Treatments, null=True, on_delete=models.CASCADE)
    file_description = models.CharField(max_length=500, blank=True)
    created = models.DateField(null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return (str(self.file_key))


    class Meta:
        verbose_name_plural = 'TreatmentFiles'


class Account(models.Model):
    account_key = models.AutoField(primary_key=True)
    invoice_no = models.CharField(max_length=300, blank=True)
    # description = models.CharField(max_length=500, blank=True)
    teeth = models.CharField(max_length=500, blank=True)
    created = models.DateField(null=True)
    is_bill= models.BooleanField(default=False)
    appointment = models.ForeignKey(Appointment, null=True, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True, null=True)
    # total_cost = models.CharField(max_length=500, blank=True)
    # net_cost = models.CharField(max_length=500, blank=True)
    discount = models.CharField(max_length=500, blank=True)


    def __str__(self):
        return (str(self.account_key))

    def total(self):
        total = Decimal('0.00')
        for item in self.items.all():
            total = total + item.total()
            after_discount = float(total) - float(total)*float((self.discount))*0.01
        return {"total_cost":float(total), "net_cost":after_discount}

    class Meta:
        verbose_name_plural = 'Accounts'


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Account, related_name='items', null=True, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.DecimalField(max_digits=8, decimal_places=2, default=1)

    def total(self):
        total = Decimal(str(self.unit_price * self.quantity))
        return total.quantize(Decimal('0.01'))

    def __unicode__(self):
        return self.description

class Bill(models.Model):
    bill_key = models.AutoField(primary_key=True)
    estimate = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
