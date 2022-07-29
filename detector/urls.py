from . import views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_custom, name='logout'),
    
    path('crear_paciente/', views.create_paciente, name='crear_paciente'),
    path('paciente/<int:id_paciente>', views.ver_paciente, name='ver_paciente'),
    path('paciente/<int:id_paciente>/edit', views.editar_paciente, name='editar_paciente'),
    path('paciente/<int:id_paciente>/delete', views.borrar_paciente, name='borrar_paciente'),

    path('paciente/<int:id_paciente>/subir_radiografia', views.subir_radiografia, name='subir_radiografias'),
    path('paciente/<int:id_paciente>/resultado/<int:id_radiografia>', views.resultado, name='resultado')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
