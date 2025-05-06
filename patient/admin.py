from django.contrib import admin

from .models import Patient, Notification

class PatientAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "full_name",
        "email",
        "mobile",
        "gender",
        "dob",
    ]

class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        "patient",
        "appointment",
        "category",
        "seen",
        "date",
    ]

admin.site.register(Patient, PatientAdmin)
admin.site.register(Notification, NotificationAdmin)