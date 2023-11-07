from django.contrib import admin
from .models import (Doctor,Patient,Conditions,Patients_Detail,Doctors_Detail,Appointment,LabReport,Bill,Discharge)


admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Conditions)
admin.site.register(Patients_Detail)
admin.site.register(Doctors_Detail)
admin.site.register(Appointment)
admin.site.register(LabReport)
admin.site.register(Bill)
admin.site.register(Discharge)

# Register your models here.
