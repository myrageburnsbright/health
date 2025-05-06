from django.shortcuts import render

# Create your views here.
def index_view (request):
    return render(request, 'base/index.html')

def service_detail_view(request, service_id):
    return render(request, 'base/service_detail.html')