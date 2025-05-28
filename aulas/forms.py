from django import forms
from .models import Aula

class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = [
            'codigo_aula', 'descripcion', 'capacidad',
            'estatus', 'sede', 'serial'
        ]
