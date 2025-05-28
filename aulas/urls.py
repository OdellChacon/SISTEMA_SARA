from django.urls import path
from . import views
from .views import eliminar_aula, importar_aulas, exportar_aulas, eliminar_seleccionados, obtener_todos_los_ids

urlpatterns = [
    path('', views.aulas_list, name='aulas_list'),
    path('registrar/', views.registrar_aula, name='registrar_aula'),
    path('editar/<int:aula_id>/', views.editar_aula, name='editar_aula'),  # Ruta para editar aula
    path('aulas/eliminar/<int:aula_id>/', eliminar_aula, name='eliminar_aula'),
    path('eliminar/<int:aula_id>/', views.eliminar_aula, name='eliminar_aula'),
    # Agregar más rutas si es necesario
    path('importar/', importar_aulas, name='cargar_aulas'),
    path('exportar/<str:format>/<str:scope>/', exportar_aulas, name='exportar_aulas'),
    path('eliminar_seleccionados/', eliminar_seleccionados, name='eliminar_seleccionados'),
    path('obtener_todos_los_ids/', obtener_todos_los_ids, name='obtener_todos_los_ids'),
]
