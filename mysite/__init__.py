from django.contrib import admin
from django.contrib.admin import sites

class PsylabAdminSite(admin.AdminSite):
    site_header = "Dentee Admin"

psyadmin = PsylabAdminSite(name="psyadmin")
admin.site = psyadmin
sites.site = psyadmin
