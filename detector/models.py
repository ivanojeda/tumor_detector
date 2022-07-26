from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()

class Paciente(models.Model):
    nombre = models.CharField('nombre', max_length=30)
    apellidos = models.CharField('apellidos', max_length=60)
    dni = models.CharField('dni', max_length=15)
    email = models.CharField('email', max_length=15)
    comentario = models.TextField('comentario')
    medico = models.ForeignKey(User, on_delete=models.CASCADE)

class Radiografia(models.Model):
    img_orig = models.BinaryField(upload_to='img', height_field=256, width_field=256)
    img_detectado = models.BinaryField(upload_to='img', height_field=256, width_field=256)
    fecha = models.DateTimeField('fecha')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
