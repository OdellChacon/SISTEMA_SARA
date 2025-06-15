from django import forms
from .models import Materia

class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ['codigo_materia', 'descripcion', 'carrera', 'trayecto', 'trimestre']
        widgets = {
            'codigo_materia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código de la materia'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción'}),
            'carrera': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Carrera'}),
            'trayecto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Trayecto'}),
            'trimestre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Trimestre'}),
        }
