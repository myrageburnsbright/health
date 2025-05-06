from django.shortcuts import render, redirect
from .models import Service, Appointment, Billing
from physician.models import Doctor
from patient.models import Patient
from django.contrib.auth.decorators import login_required
from decimal import Decimal

# Create your views here.
def index_view(request):
    sevices = Service.objects.all()
    context = {"services": sevices}
    return render(request, "base/index.html", context=context)


def service_detail_view(request, service_id):
    service = Service.objects.get(id=service_id)
    context = {"service": service}
    return render(request, "base/service_detail.html", context=context)


@login_required
def book_appointment(request, service_id, doctor_id):
    patient = Patient.objects.get(user=request.user)
    doctor = Doctor.objects.get(id=doctor_id)
    service = Service.objects.get(id=service_id)

    if request.method == "POST": 
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        issueses = request.POST.get("issueses")
        symptoms = request.POST.get("symptoms")

        patient.full_name = full_name
        patient.email = email
        patient.mobile = mobile
        patient.address = address
        patient.gender = gender
        patient.dob = dob
        patient.save()

        appointment = Appointment.objects.create(
            patient = patient,
            doctor = doctor,
            service = service,
            issues = issueses,
            symptoms = symptoms,
            appointment_date = doctor.next_appointment_date
        )

        billing = Billing()
        billing.appointment = appointment
        billing.patient = patient
        billing.sub_total = service.cost
        billing.tax = appointment.service.cost * Decimal(0.13)
        billing.total = billing.sub_total + billing.tax
        billing.status = "Не оплачено"
        billing.save()

        return redirect("base:checkout", billing_id=billing.billing_id) 
    context = {"service":service, "doctor":doctor, "patient":patient}
    return render(request, "base/book_appointment.html", context=context)

def checkout_view(request, billing_id):
    billing = Billing.objects.get(billing_id=billing_id)
    context = {"billing":billing}
    return render(request, "base/checkout.html", context=context)