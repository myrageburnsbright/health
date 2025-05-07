from django.urls import path

app_name = "physician"

from physician import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("appointments/", views.appointments, name="appointments"),
    path(
        "appointments/<appointment_id>",
        views.appointment_detail,
        name="appointment_detail",
    ),
    path(
        "cancel-appointments/<appointment_id>",
        views.cancel_appointment,
        name="cancel_appointment",
    ),
    path(
        "complete-appointments/<appointment_id>",
        views.complete_appointment,
        name="complete_appointment",
    ),
    path(
        "activate-appointments/<appointment_id>",
        views.activate_appointment,
        name="activate_appointment",
    ),
]
