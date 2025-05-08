
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('userauths/', include('userauths.urls', namespace='userauths')),
    path("", include("base.urls", namespace="base")),
    path("physician/", include("physician.urls", namespace="physician")),
    path("patient/", include("patient.urls", namespace="patient")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)