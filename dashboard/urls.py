from django.urls import path, include
from django.contrib import admin
from . import views
from .views import CustomLoginView
from SARA.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docentes/', include('docentes.urls')),
    path('aulas/', include('aulas.urls')),  # Incluir las rutas de aulas
    path('materias/', include('materias.urls')),  # Incluir las rutas de materias
    path('admin_dash/', views.dashboard, name='admin_dashboard'),  # Dashboard de administradores
    path('doc_dash/', views.dashboard_docente, name='dashboard_docente'),  # Dashboard de docentes
    path('configuracion/', views.configuracion, name='configuracion'),
    path('', login_view, name='login'),
]