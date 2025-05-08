from textwrap import wrap
from django.shortcuts import render, redirect
from django.template import context
from django.core.exceptions import PermissionDenied
from django.utils.functional import wraps
from base import models as base_models
from .models import Patient
from django.contrib.auth.decorators import login_required

from patient import models as patient_models

from django.contrib import messages
from django.db import models

@login_required
def dashboard(request):
    patient = Patient.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(patient=patient)
    notifications = patient_models.Notification.objects.filter(patient=patient)

    total_spend = base_models.Billing.objects.filter(patient=patient).aggregate(total_spend = models.Sum('total'))

    context = {
        "appointments": appointments,
        "notifications": notifications,
        "total_spend": total_spend}
    return render(request, "patient/dashboard.html", context=context)

@login_required
def appointments(request):
    patient = Patient.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(patient=patient)

    context = {"appointments": appointments}
    return render(request, "patient/appointments.html", context=context)


@login_required
def appointment_detail(request, appointment_id):
    patient = Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, patient=patient
    )

    medical_record = base_models.MedicalRecord.objects.filter(appointment=appointment)
    lab_tests = base_models.LabTest.objects.filter(appointment=appointment)
    prescriptions = base_models.Prescription.objects.filter(appointment=appointment)
    context = {
        "appointment": appointment,
        "medical_record": medical_record,
        "lab_tests": lab_tests,
        "prescriptions": prescriptions,
    }

    return render(request, "patient/appointment_detail.html", context=context)

@login_required
def payments(request):
    patient = Patient.objects.get(user=request.user)
    payments = base_models.Billing.objects.filter(patient=patient, status = "Оплачено")
    context = {"payments": payments}
    return render(request, "patient/payments.html", context=context)

@login_required
def cancel_appointment(request, appointment_id):
    patient= Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, patient=patient
    )
    appointment.status = "Отменено"
    appointment.save()
    messages.success(request, "Appointment Отменено")
    return redirect("patient:appointment_detail", appointment.appointment_id)


@login_required
def complete_appointment(request, appointment_id):
    doctor = physician_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, doctor=doctor
    )
    appointment.status = "Выполнено"
    appointment.save()
    messages.success(request, "Прием успешно выполнен")
    return redirect("physician:appointment_detail", appointment.appointment_id)


@login_required
def activate_appointment(request, appointment_id):
    patient = Patient.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(
        appointment_id=appointment_id, patient=patient
    )
    appointment.status = "Запланировано"
    appointment.save()
    messages.success(request, "Appointment Запланировано")
    return redirect("patient:appointment_detail", appointment.appointment_id)    

    
@login_required
def notifications(request):
    patient = Patient.objects.get(user=request.user)
    notifications = patient_models.Notification.objects.filter(patient=patient, seen=False)
    context = {"notifications": notifications}
    return render(request, "patient/notifications.html", context=context)

@login_required
def mark_as_read_notifications(request, id):
    patient = Patient.objects.get(user=request.user)
    notification = patient_models.Notification.objects.get(id=id, patient=patient)
    notification.seen = True
    notification.save()
    messages.success(request, "Уведомление прочитано")
    return redirect("patient:notifications")

@login_required
def profile(request):
    patient = Patient.objects.get(user=request.user)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        image = request.FILES.get("image")
        phone = request.POST.get("mobile")
        city = request.POST.get("country")
        bio = request.POST.get("bio")

        patient.full_name = full_name
        patient.phone = phone
        patient.city = city
        patient.bio = bio

        if image is not None:
            patient.image = image

        patient.save()
        messages.success(request, "Профиль успешно обновлен")
        return redirect("patient:profile")

    patient_dob = patient.dob.strftime("%Y-%m-%d")
    context = {"patient": patient, "formatted_dob": patient_dob}
    return render(request, "patient/profile.html", context=context)