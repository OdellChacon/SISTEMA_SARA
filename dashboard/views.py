from docentes.models import Docente
from clases.models import Clase, Asistencia, Incumplimiento
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, permission_required
from docentes.forms import EmailAuthenticationForm  # Asegúrate de importar el correcto
from django.urls import reverse_lazy

@login_required
def dashboard(request):
    # Contar el número de docentes
    docentes_count = Docente.objects.filter(rol=2).count()
    
    # Contar las clases, asistencias e incumplimientos
    clases_count = Clase.objects.count()
    asistencias_count = Asistencia.objects.count()
    # Corrige el conteo de incumplimientos: solo cuenta los distintos incumplimientos
    incumplimientos_count = Incumplimiento.objects.all().count()

    # Mantener el ejemplo para asistencia promedio
    asistencia_promedio = 85  # Este es solo un ejemplo

    return render(request, 'dashboard/dashboard.html', {
        'docentes_count': docentes_count,
        'clases_count': clases_count,
        'asistencias_count': asistencias_count,
        'incumplimientos_count': incumplimientos_count,
        'asistencia_promedio': asistencia_promedio,
    })

@login_required
def configuracion(request):
    return render(request, 'dashboard/configuracion.html')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = EmailAuthenticationForm

    def get_success_url(self):
        user = self.request.user
        if hasattr(user, 'rol'):
            if user.rol == 1:
                return reverse_lazy('admin_dashboard')
            elif user.rol == 2:
                return reverse_lazy('dashboard_docente')
        return reverse_lazy('admin_dashboard')  # Fallback
    
@login_required
def dashboard_docente(request):
    return render(request, "dashboard/dashboardDocente.html")