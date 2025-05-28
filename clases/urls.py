from django.urls import path
from .views import calendario, clases_json, registrar_clase, registrar_asistencia, listar_asistencias, listar_incumplimientos, eliminar_clase, reprogramar_clase

urlpatterns = [
    path('calendario/', calendario, name='calendario'),
    path('clases-json/', clases_json, name='clases_json'),
    path('registrar-clase/', registrar_clase, name='registrar_clase'),
    path('registrar-asistencia/', registrar_asistencia, name='registrar_asistencia'),
    path('listar-asistencias/', listar_asistencias, name='listar_asistencias'),
    path('listar-incumplimientos/', listar_incumplimientos, name='listar_incumplimientos'),
    path('eliminar-clase/', eliminar_clase, name='eliminar_clase'),
    path('reprogramar-clase/', reprogramar_clase, name='reprogramar_clase'),
]
