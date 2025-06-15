from django.contrib import admin
from .models import Clase, Asistencia, Incumplimiento

@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'docente', 'materia', 'fecha', 'hora_inicio', 'hora_fin', 'aula')
    list_filter = ('docente', 'materia', 'aula', 'fecha')
    search_fields = ('docente__nombre', 'materia__descripcion', 'aula__codigo_aula')

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'clase', 'comentarios')
    search_fields = ('clase__materia__descripcion',)

@admin.register(Incumplimiento)
class IncumplimientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'clase', 'docente', 'fecha_reporte')
    search_fields = ('clase__materia__descripcion', 'docente__nombre')
