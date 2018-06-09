from django.conf.urls import include, url

import users
from .views import patient_view, treatment_view, treatmentlist_view, account_view,appointment_view, invoice_view, treatment_file_view, patientfilter_view, appointmentfilter_view, bill_invoice_view, bill_view, getuser_view, appointmentmessage_view, treatappointmentfilter_view, treatment_file_filter_view, appointment_estimate_filter_view, treatpatientfilter_view, user_details_view

urlpatterns = [
    url(r'^patient/', patient_view),
    url(r'^treatment/', treatment_view),
    url(r'^treatmentlist/', treatmentlist_view),
    url(r'^appointment/', appointment_view),
    url(r'^account/', account_view),
    url(r'^invoice/', invoice_view),
    url(r'^treatmentfile/', treatment_file_view),
    url(r'^patientfilter/', patientfilter_view),
    url(r'^appointmentfilter/', appointmentfilter_view),
    url(r'^billpost/', bill_invoice_view),
    url(r'^bill/', bill_view),
    url(r'^getusers/', getuser_view),
    url(r'^appointmentmessage/', appointmentmessage_view),
    url(r'^treatappointmentfilter/', treatappointmentfilter_view),
    url(r'^treatmentfilefilter/', treatment_file_filter_view),
    url(r'^appointmentestimatefilter/', appointment_estimate_filter_view),
    url(r'^treatpatientfilter/', treatpatientfilter_view),
    url(r'^userdetails/', user_details_view),
]
