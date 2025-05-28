from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Docente, Administrador

class DocenteForm(UserCreationForm):  # Heredamos de UserCreationForm para manejar contraseñas
    class Meta:
        model = Docente
        fields = ['nombre', 'apellido', 'cedula', 'password1', 'password2', 'activo', 'rol']  # Incluimos username y contraseñas
        widgets = {
            'nombre': forms.TextInput(attrs={'required': True}),
            'apellido': forms.TextInput(attrs={'required': True}),
            'cedula': forms.TextInput(attrs={'required': True}),
            'activo': forms.CheckboxInput(),
            'rol': forms.Select(),
        }

class DocenteUpdateForm(forms.ModelForm):  # Formulario para actualizar datos del docente
    class Meta:
        model = Docente
        fields = ['nombre', 'apellido', 'cedula', 'activo', 'rol']  # Excluimos las contraseñas
        widgets = {
            'nombre': forms.TextInput(attrs={'required': True}),
            'apellido': forms.TextInput(attrs={'required': True}),
            'cedula': forms.TextInput(attrs={'required': True}),
            'activo': forms.CheckboxInput(),
            'rol': forms.Select(),
        }

#ADMINISTRADORES
class AdminForm(UserCreationForm):  # Heredamos de UserCreationForm para manejar contraseñas
    class Meta:
        model = Administrador
        fields = ['nombre', 'apellido', 'cedula', 'password1', 'password2', 'activo', 'rol']  # Incluimos username y contraseñas
        widgets = {
            'nombre': forms.TextInput(attrs={'required': True}),
            'apellido': forms.TextInput(attrs={'required': True}),
            'cedula': forms.TextInput(attrs={'required': True}),
            'activo': forms.CheckboxInput(),
            'rol': forms.Select(),
        }

class AdminUpdateForm(forms.ModelForm):  # Formulario para actualizar datos del docente
    class Meta:
        model = Administrador
        fields = ['nombre', 'apellido', 'cedula', 'activo', 'rol']  # Excluimos las contraseñas
        widgets = {
            'nombre': forms.TextInput(attrs={'required': True}),
            'apellido': forms.TextInput(attrs={'required': True}),
            'cedula': forms.TextInput(attrs={'required': True}),
            'activo': forms.CheckboxInput(),
            'rol': forms.Select(),
        }

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Cédula"),
        widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"})
    )