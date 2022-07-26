from django.contrib import admin
from django.urls import path, include
from detector import views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('detector.urls')),
    path('/admin', admin.site.urls),
    path('', RedirectView.as_view(url='/detector/', permanent=True)),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
