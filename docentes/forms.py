from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Docente, Administrador

class DocenteForm(UserCreationForm):  # Heredamos de UserCreationForm para manejar contraseñas
    class Meta:
        model = Docente
        fields = ['nombre', 'apellido', 'correo', 'telefono', 'cedula', 'password1', 'password2', 'activo']  # Incluimos username y contraseñas
        widgets = {
            'nombre': forms.TextInput(attrs={'required': True}),
            'apellido': forms.TextInput(attrs={'required': True}),
            'correo': forms.EmailInput(attrs={'required': True}),
            'telefono': forms.TextInput(attrs={'required': True}),
            'cedula': forms.TextInput(attrs={'required': True}),
            'activo': forms.CheckboxInput(),
        }

class DocenteUpdateForm(forms.ModelForm):  # Formulario para actualizar datos del docente
    class Meta:
        model = Docente
        fields = ['nombre', 'apellido', 'correo', 'telefono', 'cedula', 'activo']  # Excluimos las contraseñas
        widgets = {
            'nombre': forms.TextInput(attrs={'required': True}),
            'apellido': forms.TextInput(attrs={'required': True}),
            'correo': forms.EmailInput(attrs={'required': True}),
            'telefono': forms.TextInput(attrs={'required': True}),
            'cedula': forms.TextInput(attrs={'required': True}),
            'activo': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacemos que el campo 'correo' sea de solo lectura si es necesario
        self.fields['correo'].widget.attrs['readonly'] = True
        
#ADMINISTRADORES
class AdminForm(UserCreationForm):  # Heredamos de UserCreationForm para manejar contraseñas
    class Meta:
        model = Administrador
        fields = ['nombre', 'apellido', 'correo', 'telefono', 'cedula', 'password1', 'password2', 'activo']  # Incluimos username y contraseñas
        widgets = {
            'nombre': forms.TextInput(attrs={'required': True}),
            'apellido': forms.TextInput(attrs={'required': True}),
            'correo': forms.EmailInput(attrs={'required': True}),
            'telefono': forms.TextInput(attrs={'required': True}),
            'cedula': forms.TextInput(attrs={'required': True}),
            'activo': forms.CheckboxInput(),
        }

class AdminUpdateForm(forms.ModelForm):  # Formulario para actualizar datos del docente
    class Meta:
        model = Administrador
        fields = ['nombre', 'apellido', 'correo', 'telefono', 'cedula', 'activo']  # Excluimos las contraseñas
        widgets = {
            'nombre': forms.TextInput(attrs={'required': True}),
            'apellido': forms.TextInput(attrs={'required': True}),
            'correo': forms.EmailInput(attrs={'required': True}),
            'telefono': forms.TextInput(attrs={'required': True}),
            'cedula': forms.TextInput(attrs={'required': True}),
            'activo': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacemos que el campo 'correo' sea de solo lectura si es necesario
        self.fields['correo'].widget.attrs['readonly'] = True

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label=_("Correo electrónico"),
        widget=forms.EmailInput(attrs={"autofocus": True, "class": "form-control"})
    )