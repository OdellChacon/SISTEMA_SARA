from django.contrib import admin
from .models import Materia

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ('codigo_materia', 'descripcion', 'carrera', 'trayecto', 'trimestre')
    search_fields = ('codigo_materia', 'descripcion', 'carrera', 'trayecto', 'trimestre')
    list_filter = ('carrera', 'trayecto', 'trimestre')
