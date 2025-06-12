from django.urls import path
from . import views

urlpatterns = [
    path('', views.materias_list, name='materias_list'),
    path('registrar/', views.registrar_materia, name='registrar_materia'),
    path('editar/<int:materia_id>/', views.editar_materia, name='editar_materia'),
    path('eliminar/<int:materia_id>/', views.eliminar_materia, name='eliminar_materia'),
    path('eliminar_seleccionados/', views.eliminar_seleccionados, name='eliminar_materias_seleccionadas'),
    path('importar/', views.importar_materias, name='importar_materias'),
    path('exportar/<str:format>/<str:scope>/', views.exportar_materias, name='exportar_materias'),
    path('obtener_todos_los_ids/', views.obtener_todos_los_ids, name='obtener_todos_los_ids'),
    path('buscar/', views.buscar_materias, name='buscar_materias'),
]
