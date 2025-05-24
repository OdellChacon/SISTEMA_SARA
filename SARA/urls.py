from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', include('dashboard.urls')),  # Incluye las URLs del dashboard
    path('docentes/', include('docentes.urls')),
    path('materias/', include('materias.urls')),
    path('aulas/', include('aulas.urls')),
    path('clases/', include('clases.urls')),
]

# Configuración para servir archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)