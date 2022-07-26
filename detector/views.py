from imp import reload
from django.shortcuts import render, redirect
from datetime import date
from hashlib import new
from django.http import HttpResponse, HttpResponseRedirect
from types import new_class
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators  import login_required
from django.contrib.auth import logout, get_user_model, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

from .decorators import user_not_authenticated
from .form import pacienteForm, userRegistrationForm
from .models import Paciente, Radiografia

def validador_dni(dni):
    tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
    dig_ext = "XYZ"
    reemp_dig_ext = {'X':'0', 'Y':'1', 'Z':'2'}
    numeros = "1234567890"
    dni = dni.upper()
    if len(dni) == 9:
        dig_control = dni[8]
        dni = dni[:8]
        if dni[0] in dig_ext:
            dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
        return len(dni) == len([n for n in dni if n in numeros]) \
            and tabla[int(dni)%23] == dig_control
    return False


@user_not_authenticated
def register(request):
    if request.user.is_authenticated:
        return redirect('/register')
    if request.method == "POST":
        form = userRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/index')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = userRegistrationForm()
    return render(
        request=request,
        template_name= 'register.html',
        context={'form': form}
    )

@user_not_authenticated
def login(request):
    if request.user.is_authenticated:
        return redirect("/index")

    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                return redirect("/index")

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = AuthenticationForm()

    return render(
        request=request,
        template_name="login.html",
        context={"form": form}
        )

@login_required
def logout_custom(request):
    logout(request)
    messages.info(request, "Se ha cerrado la sesion correctamente")
    return redirect('/login')

@login_required
def index(request):
    pacientes = Paciente.objects.filter(medico_id=request.user.id)
    return render(
        request=request,
        template_name="index.html",
        context={"pacientes": pacientes}
    )


# VIEWS DE PACIENTES (CREAR, BORRAR, EDITAR Y VER)

@login_required
def create_paciente(request):
    error = {}
    if request.method == "POST":
        if validador_dni(request.POST['dni']) == False:
            error['dni']="DNI incorrecto"
        else:
            form = pacienteForm(request.POST)
            if form.is_valid():
                paciente = Paciente()
                paciente.nombre = form.cleaned_data['nombre']
                paciente.apellidos = form.cleaned_data['apellidos']
                paciente.dni = form.cleaned_data['dni']
                paciente.email = form.cleaned_data['email']
                paciente.comentario = form.cleaned_data['comentario']
                paciente.medico_id = request.user.id
                paciente.save()
                return redirect('/index')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
    form = pacienteForm()
    return render(
        request=request,
        template_name="paciente/create.html",
        context={"error": error}
        )

@login_required
def ver_paciente(request, id_paciente):
    return render(
        request=request,
        template_name="paciente/view.html",
    )

@login_required
def editar_paciente(request, id_paciente):
    paciente = Paciente.objects.get(pk=id_paciente)
    error = {}
    if request.method == "POST":
        if validador_dni(request.POST['dni']) == False:
            error['dni']="DNI incorrecto"
        else:
            form = pacienteForm(request.POST)
            if form.is_valid():
                paciente.nombre = form.cleaned_data['nombre']
                paciente.apellidos = form.cleaned_data['apellidos']
                paciente.dni = form.cleaned_data['dni']
                paciente.email = form.cleaned_data['email']
                paciente.comentario = form.cleaned_data['comentario']
                paciente.medico_id = request.user.id
                paciente.save()
                return redirect('/index')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
    form = pacienteForm()
    return render(
        request=request,
        template_name="paciente/create.html",
        context={"paciente": paciente}
    )

@login_required
def borrar_paciente(request, id_paciente):
    paciente = Paciente.objects.get(pk=id_paciente)
    paciente.delete()
    return redirect('/index')

@login_required
def subir_radiografia(request):
    return render(
        request=request,
        template_name="radiografia/subir_radiografia.html",
    )