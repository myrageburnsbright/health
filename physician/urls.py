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
    path(
        "add-medical-record/<appointment_id>",
        views.add_medical_record,
        name="add_medical_record",
    ),
    path(
        "edit-medical-record/<appointment_id>/<medical_record_id>",
        views.edit_medical_record,
        name="edit_medical_record",
    ),
    path(
        "add-lab-test/<appointment_id>",
        views.add_lab_test,
        name="add_lab_test",
    ),
    path(
        "edit-lab-test/<appointment_id>/<lab_test_id>",
        views.edit_lab_test,
        name="edit_lab_test",
    ),
    path(
        "add-prescription/<appointment_id>",
        views.add_prescription,
        name="add_prescription",
    ),
    path(
        "edit-prescription/<appointment_id>/<prescription_id>",
        views.edit_prescription,
        name="edit_prescription",
    ),
    path("payments/", views.payments, name="payments"),

]
