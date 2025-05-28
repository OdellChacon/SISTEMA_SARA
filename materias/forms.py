from django import forms
from .models import Materia

class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ['codigo_materia', 'descripcion', 'trayecto']
        widgets = {
            'codigo_materia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código de la materia'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
            'trayecto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Trayecto'}),
        }
