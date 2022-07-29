from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from pkg_resources import require



class userRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)

    class Meta:
        model = get_user_model()
        fields = ['username',  'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = (super(userRegistrationForm, self).save(commit=False))
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user

class pacienteForm(forms.Form):
    dni = forms.CharField(help_text='Introduce un DNI valido.', required=True)
    email = forms.EmailField(label="Correo del paciente")
    nombre = forms.CharField(label='Nombre del paciente', required=True)
    apellidos = forms.CharField(label='Apellidos del paciente', required=False)
    comentario = forms.CharField(label='Descripcion', widget=forms.Textarea, required=True)

class radigradiaForm(forms.Form):
    img_orig = forms.ImageField(label="imagen de la radiografia")
