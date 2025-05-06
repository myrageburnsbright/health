from django.urls import path

from .views import index_view, service_detail_view

app_name = "base"

urlpatterns = [
    path('', index_view, name='index'),
    path('service/<service_id>', service_detail_view, name='service_detail'),
]