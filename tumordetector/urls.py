from django.contrib import admin
from django.urls import path, include
from detector import views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('detector.urls')),
    path('/admin', admin.site.urls),
    path('', RedirectView.as_view(url='/index/', permanent=True)),
    path('detector/', RedirectView.as_view(url='/index/', permanent=True)),
]
