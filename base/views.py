from django.shortcuts import render
from .models import Service


# Create your views here.
def index_view(request):
    sevices = Service.objects.all()
    context = {"services": sevices}
    return render(request, "base/index.html", context=context)


def service_detail_view(request, service_id):
    service = Service.objects.get(id=service_id)
    context = {"service": service}
    return render(request, "base/service_detail.html", context=context)
