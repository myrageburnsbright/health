from django.shortcuts import render, redirect

from base import models as base_models

from django.contrib.auth.decorators import login_required

from physician import models as physician_models
from django.contrib import messages
@login_required
def dashboard(request):

    doctor = physician_models.Doctor.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(doctor=doctor)
    notifications = physician_models.Notification.objects.filter(doctor=doctor) 

    context = {
        "appointments": appointments,
        "notifications": notifications,
    }
    return render(request, "physician/dashboard.html", context=context)

@login_required
def appointments(request):
    doctor = physician_models.Doctor.objects.get(user=request.user)
    appointments = base_models.Appointment.objects.filter(doctor=doctor)

    context = {"appointments": appointments}
    return render(request, "physician/appointments.html", context=context)

@login_required
def appointment_detail(request, appointment_id):
    doctor = physician_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)

    medical_record = base_models.MedicalRecord.objects.filter(appointment=appointment)
    lab_tests = base_models.LabTest.objects.filter(appointment=appointment)
    prescriptions = base_models.Prescription.objects.filter(appointment=appointment)
    context = {
        "appointment": appointment,
        "medical_record": medical_record,
        "lab_tests": lab_tests,
        "prescriptions": prescriptions
    }

    return render(request, "physician/appointment_detail.html", context=context)

@login_required
def cancel_appointment(request, appointment_id):
    doctor = physician_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    appointment.status = 'Отменено'
    appointment.save()
    messages.success(request, 'Appointment Отменено')
    return redirect('physician:appointment_detail', appointment.appointment_id)

@login_required
def complete_appointment(request, appointment_id):
    doctor = physician_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    appointment.status = 'Выполнено'
    appointment.save()
    messages.success(request, 'Прием успешно выполнен')
    return redirect('physician:appointment_detail', appointment.appointment_id)

@login_required
def activate_appointment(request, appointment_id):
    doctor = physician_models.Doctor.objects.get(user=request.user)
    appointment = base_models.Appointment.objects.get(appointment_id=appointment_id, doctor=doctor)
    appointment.status = 'Запланировано'
    appointment.save()
    messages.success(request, 'Appointment Запланировано')
    return redirect('physician:appointment_detail', appointment.appointment_id)