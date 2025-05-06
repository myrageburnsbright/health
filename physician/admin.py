from django.contrib import admin
from .models import Doctor, Notification


class DoctorAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "full_name",
        "phone",
        "city",
        "specialization",
        "qualification",
        "year_of_exp",
        "next_appointment_date",
    ]

class NotificationAdmin(admin.ModelAdmin):
    list_display = [
        "doctor",
        "appointment",
        "category",
        "seen",
        "date",
    ]
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Notification, NotificationAdmin)
