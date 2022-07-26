from . import views
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_custom, name='logout'),
    
    path('crear_paciente/', views.create_paciente, name='crear_paciente'),
    path('paciente/<int:id_paciente>', views.ver_paciente, name='ver_paciente'),
    path('paciente/<int:id_paciente>/edit', views.editar_paciente, name='editar_paciente'),
    path('paciente/<int:id_paciente>/delete', views.borrar_paciente, name='borrar_paciente'),

    path('subir_radiografia', views.subir_radiografia, name='subir_radiografias')
]
