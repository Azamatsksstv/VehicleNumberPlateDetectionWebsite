import detections.views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('detectnumberplate/', detections.views.DetectNumberPlate.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)