from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from docentes.forms import EmailAuthenticationForm
from docentes.models import BaseUser, Docente, Administrador

def login_view(request):
    login_error = False
    inactive_error = False
    must_login = request.GET.get('next') is not None  # Detecta si viene de una redirección por login_required

    if request.method == 'POST':
        print("Método POST recibido")  # Depuración
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print("Formulario válido")  # Depuración
            cedula = form.cleaned_data['username']  # Ahora username es la cédula
            password = form.cleaned_data['password']
            print(f"Datos recibidos: cedula={cedula}, password={password}")  # Depuración
            user = authenticate(request, username=cedula, password=password)
            if user:
                print(f"Usuario autenticado: {getattr(user, 'cedula', '')}")  # Depuración
                if not user.activo:
                    print("Usuario inactivo")  # Depuración
                    inactive_error = True
                else:
                    login(request, user)
                    print(f"Usuario logueado: {getattr(user, 'cedula', '')}")  # Depuración
                    # Redirigir según el tipo de usuario
                    if isinstance(user, Docente):
                        print("Redirigiendo a clases/calendario.html")  # Depuración
                        return render(request, 'clases/calendario.html')
                    else:
                        print("Redirigiendo al dashboard administrativo")  # Depuración
                        return redirect('admin_dashboard')
            else:
                print("Error: Usuario no autenticado")  # Depuración
                login_error = True
        else:
            print("Formulario inválido")  # Depuración
            print(form.errors)
    else:
        print("Método GET recibido")  # Depuración
        form = EmailAuthenticationForm()

    return render(request, 'registration/login.html', {
        'form': form,
        'login_error': login_error,
        'inactive_error': inactive_error,
        'must_login': must_login,  # Pasa la variable al template
    })

def logout_view(request):
    logout(request)
    return redirect(reverse('login'))