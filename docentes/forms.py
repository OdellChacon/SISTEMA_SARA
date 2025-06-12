from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Docente, Administrador

class DocenteForm(UserCreationForm):  # Heredamos de UserCreationForm para manejar contraseñas
    class Meta:
        model = Docente
        fields = ['nombre', 'apellido', 'cedula', 'password1', 'password2', 'activo']  # Eliminado 'rol'
        widgets = {
            'nombre': forms.TextInput(attrs={'required': True}),
            'apellido': forms.TextInput(attrs={'required': True}),
            'cedula': forms.TextInput(attrs={'required': True}),
            'activo': forms.CheckboxInput(),
            # 'rol': forms.Select(),  # Eliminado
        }

class DocenteUpdateForm(forms.ModelForm):  # Formulario para actualizar datos del docente
    class Meta:
        model = Docente
        fields = ['nombre', 'apellido', 'cedula', 'activo']  # Eliminado 'rol'
        widgets = {
            'nombre': forms.TextInput(attrs={'required': True}),
            'apellido': forms.TextInput(attrs={'required': True}),
            'cedula': forms.TextInput(attrs={'required': True}),
            'activo': forms.CheckboxInput(),
            # 'rol': forms.Select(),  # Eliminado
        }

#ADMINISTRADORES
class AdminForm(UserCreationForm):  # Heredamos de UserCreationForm para manejar contraseñas
    class Meta:
        model = Administrador
        fields = ['nombre', 'apellido', 'cedula', 'password1', 'password2', 'activo']  # Eliminado 'rol'
        widgets = {
            'nombre': forms.TextInput(attrs={'required': True}),
            'apellido': forms.TextInput(attrs={'required': True}),
            'cedula': forms.TextInput(attrs={'required': True}),
            'activo': forms.CheckboxInput(),
            # 'rol': forms.Select(),  # Eliminado
        }

class AdminUpdateForm(forms.ModelForm):  # Formulario para actualizar datos del docente
    class Meta:
        model = Administrador
        fields = ['nombre', 'apellido', 'cedula', 'activo']  # Eliminado 'rol'
        widgets = {
            'nombre': forms.TextInput(attrs={'required': True}),
            'apellido': forms.TextInput(attrs={'required': True}),
            'cedula': forms.TextInput(attrs={'required': True}),
            'activo': forms.CheckboxInput(),
            # 'rol': forms.Select(),  # Eliminado
        }

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Cédula"),
        widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"})
    )