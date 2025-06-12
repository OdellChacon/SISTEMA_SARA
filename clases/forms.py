from django import forms
from .models import Clase

class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = ['docente', 'materia', 'hora_inicio', 'hora_fin', 'aula']
        widgets = {
            'docente': forms.Select(attrs={'class': 'form-control'}),
            'materia': forms.Select(attrs={'class': 'form-control'}), 
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'aula': forms.Select(attrs={'class': 'form-control'}),  
        }


class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ['foto_clase', 'foto_lista', 'comentarios']
        widgets = {
            'foto_clase': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'foto_lista': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
