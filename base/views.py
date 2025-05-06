from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Service, Appointment, Billing
from physician.models import Doctor, Notification
from patient.models import Patient
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
import stripe
from django.urls import reverse
from django.conf import settings
from patient.models import Notification as PatientNotification
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

@login_required
def checkout_view(request, billing_id):
    billing = Billing.objects.get(billing_id=billing_id)
    stripe_public_key = settings.STRIPE_PUBLIC_KEY

    context = {"billing":billing, "stripe_public_key":stripe_public_key} 
    return render(request, "base/checkout.html", context=context)

@csrf_exempt
def stripe_payment(request, billing_id):
    billing = Billing.objects.get(billing_id=billing_id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email=request.user.email,
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': "Оплата услуги " + billing.patient.full_name,
                    },
                    'unit_amount': int(billing.total * 100),
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse("base:stripe_payment_verify", args=[billing_id]))+"?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("base:stripe_payment_verify", args=[billing_id]))
    )

    return JsonResponse({'sessionId': checkout_session.id})

@login_required
def stripe_payment_verify(request, billing_id):
    billing = Billing.objects.get(billing_id=billing_id)
    session_id = request.GET.get('session_id')
    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == 'paid':
        if billing.status == "Не оплачено":
            billing.status = "Оплачено"
            billing.save()
            billing.appointment.status = "Выполнено"
            billing.appointment.save()

            Notification.objects.create(
                doctor = billing.appointment.doctor,
                appointment = billing.appointment,
                category = "Новая запись",
            )

            PatientNotification.objects.create(
                patient = billing.appointment.patient,
                appointment = billing.appointment,
                category = "Запись создана",
            )
            return redirect(f"/payment_status/{billing_id}/?payment_status=paid")
    else:
        return redirect(f"/payment_status/{billing_id}/?payment_status=failed")

@login_required
def payment_status_view(request, billing_id):
    billing = Billing.objects.get(billing_id=billing_id)
    payment_status = request.GET.get("payment_status")
    context = {"billing":billing, "payment_status":payment_status}
    return render(request, "base/payment_status.html", context=context)