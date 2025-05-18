from django import forms
from .models import Materia

class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = ['nombre', 'codigo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la materia'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código de la materia'}),
        }
