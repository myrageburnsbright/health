from django.urls import path

from .views import index_view, checkout_view, service_detail_view, book_appointment

app_name = "base"

urlpatterns = [
    path("", index_view, name="index"),
    path("service/<service_id>", service_detail_view, name="service_detail"),
    path(
        "book-appointment/<service_id>/<doctor_id>",
        book_appointment,
        name="book_appointment",
    ),
    path("checkout/<billing_id>", checkout_view, name="checkout"),
]
