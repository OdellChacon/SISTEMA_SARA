from django.urls import path
from . import views
from .views import *
from .views import buscar_docentes

urlpatterns = [
    path('', views.docentes_list, name='docentes_list'),
    path('registrar/', registrar_docente, name='registrar_docente'),
    
    # Ruta para editar un docente
    path('editar/<int:docente_id>/', views.editar_docente, name='editar_docente'),
    
    # Ruta para eliminar un docente
    path('eliminar/<int:docente_id>/', views.eliminar_docente, name='eliminar_docente'),


    path("exportar/<str:formato>/<str:tipo>/", exportar_docentes, name="exportar_docentes"),
    path("cargar_docentes/", views.cargar_docentes, name="cargar_docentes"),
    path("eliminar_seleccionados/", views.eliminar_seleccionados_docentes, name="eliminar_seleccionados"),
    path("obtener_todos_los_ids/", views.obtener_todos_los_ids_docentes, name="obtener_todos_los_ids_docentes"),
    path('detalle/<int:docente_id>/', views.detalle_docente, name='detalle_docente'),
    path('buscar/', buscar_docentes, name='buscar_docentes'),
    
    #Administradores
    path('listaAdministradores/', admin_list, name='admin_list'),
    path('registrarAdministrador/', registrar_admin, name='registrar_admin'),
    
    # Ruta para editar un docente
    path('editarAdministrador/<int:docente_id>/', views.editar_admin, name='editar_admin'),
    
    # Ruta para eliminar un docente
    path('eliminarAdministrador/<int:docente_id>/', views.eliminar_admin, name='eliminar_admin'),
    path('detalle/<int:docente_id>/', views.detalle_admin, name='detalle_admin'),


]
