from django.shortcuts import render
from django.http import JsonResponse
from .models import Clase, Docente, Asistencia, Incumplimiento
from materias.models import Materia
from aulas.models import Aula
from django.utils.timezone import now, localtime, make_aware
from django.core.paginator import Paginator
from datetime import date, time, datetime  # ✅ Importar datetime para convertir cadenas ISO a objetos de fecha
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json

def verificar_incumplimientos():
    # ✅ Verificar clases cuya hora de fin ya pasó y no tienen asistencia registrada
    clases = Clase.objects.filter(fecha__lte=localtime(now()).date(), hora_fin__lt=localtime(now()).time())
    for clase in clases:
        if not clase.asistencias.exists():
            Incumplimiento.objects.get_or_create(clase=clase, docente=clase.docente)

def calendario(request):
    docentes = Docente.objects.all().values('id', 'nombre', 'cedula')
    materias = Materia.objects.all().values('id', 'nombre')
    aulas = Aula.objects.all().values('id', 'tipo', 'numero', 'departamento')

    clases = Clase.objects.all().values(
        'id', 
        'materia__id', 
        'materia__nombre', 
        'docente__id', 
        'docente__nombre', 
        'aula__id', 
        'fecha', 
        'hora_inicio', 
        'hora_fin'
    )

    clases_list = []
    for clase in clases:
        clase_dict = dict(clase)
        fecha_clase = clase_dict['fecha']
        hora_inicio_clase = clase_dict['hora_inicio']
        hora_fin_clase = clase_dict['hora_fin']

        # ✅ Asegurar que los objetos datetime sean conscientes de la zona horaria
        fecha_hora_inicio = make_aware(datetime.combine(fecha_clase, hora_inicio_clase))
        fecha_hora_fin = make_aware(datetime.combine(fecha_clase, hora_fin_clase))

        # ✅ Incluir todas las clases (activas e inactivas)
        clase_dict['fecha'] = fecha_clase.isoformat()
        clase_dict['hora_inicio'] = fecha_hora_inicio.time().isoformat()
        clase_dict['hora_fin'] = fecha_hora_fin.time().isoformat()
        clases_list.append(clase_dict)

    docentes_json = json.dumps(list(docentes))
    materias_json = json.dumps(list(materias))
    aulas_json = json.dumps(list(aulas))
    clases_json = json.dumps(clases_list)  # ✅ Incluir todas las clases

    return render(request, 'clases/calendario.html', {
        'docentes_json': docentes_json,
        'materias_json': materias_json,
        'aulas_json': aulas_json,
        'clases_json': clases_json,
    })


@csrf_exempt
def registrar_clase(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            docente = Docente.objects.get(id=data['docente_id'])
            materia = Materia.objects.get(id=data['materia_id'])
            aula = Aula.objects.get(id=data['aula_id'])

            # Validar que hora_inicio sea menor que hora_fin
            if data['hora_inicio'] >= data['hora_fin']:
                return JsonResponse({'status': 'error', 'message': 'La hora de inicio debe ser menor que la hora de fin.'}, status=400)

            nueva_clase = Clase.objects.create(
                docente=docente,
                materia=materia,
                aula=aula,
                fecha=data['fecha_inicio'],
                hora_inicio=data['hora_inicio'],
                hora_fin=data['hora_fin']
            )
            return JsonResponse({'status': 'success', 'message': 'Clase registrada', 'id': nueva_clase.id})  # ✅ Devolver el ID de la clase
        except (Docente.DoesNotExist, Materia.DoesNotExist, Aula.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Docente, materia o aula no encontrado'})
        except Exception as e:
            print("Error al registrar la clase:", e)
            return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@csrf_exempt
def registrar_asistencia(request):
    if request.method == 'POST':
        try:
            data = request.POST
            clase_id = data.get('clase_id')
            foto_clase = request.FILES.get('foto_clase')
            foto_lista = request.FILES.get('foto_lista')
            comentarios = data.get('comentarios', '')

            if not clase_id or not foto_clase or not foto_lista:
                return JsonResponse({'status': 'error', 'message': 'Todos los campos obligatorios deben ser completados.'}, status=400)

            clase = Clase.objects.get(id=clase_id)
            Asistencia.objects.create(
                clase=clase,
                foto_clase=foto_clase,
                foto_lista=foto_lista,
                comentarios=comentarios
            )
            return JsonResponse({'status': 'success', 'message': 'Asistencia registrada correctamente.'})
        except Clase.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Clase no encontrada.'}, status=404)
        except Exception as e:
            print("Error al registrar la asistencia:", e)
            return JsonResponse({'status': 'error', 'message': 'Error interno del servidor.'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)

def clases_json(request):
    clases = Clase.objects.all()
    eventos = []
    for clase in clases:
        eventos.append({
            'id': clase.id,
            'title': f"{clase.materia.nombre} - {clase.docente.nombre}",
            'start': f"{clase.fecha}T{clase.hora_inicio}",
            'end': f"{clase.fecha}T{clase.hora_fin}",
            'extendedProps': {
                'aula': clase.aula.nombre,
                'docente_id': clase.docente.id,
                'materia_id': clase.materia.id,
                'aula_id': clase.aula.id
            }
        })
    return JsonResponse(eventos, safe=False)

def listar_asistencias(request):
    asistencias = Asistencia.objects.select_related('clase').all()
    paginator = Paginator(asistencias, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'clases/listar_asistencias.html', {'page_obj': page_obj})

def listar_incumplimientos(request):
    verificar_incumplimientos()
    incumplimientos = Incumplimiento.objects.select_related('clase', 'docente').all()
    paginator = Paginator(incumplimientos, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'clases/listar_incumplimientos.html', {'page_obj': page_obj})

@csrf_exempt
def eliminar_clase(request):
    if request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            clase_id = data.get('id')
            if not clase_id or not str(clase_id).isdigit():  # ✅ Validar que el ID sea un número válido
                return JsonResponse({'status': 'error', 'message': 'ID de clase no válido'}, status=400)
            
            clase = Clase.objects.get(id=int(clase_id))  # ✅ Convertir el ID a entero
            clase.delete()
            return JsonResponse({'status': 'success', 'message': 'Clase eliminada'})
        except Clase.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Clase no encontrada'}, status=404)
        except Exception as e:
            print("Error al eliminar la clase:", e)
            return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@csrf_exempt
def reprogramar_clase(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            clase_id = data.get('id')
            if not clase_id or not str(clase_id).isdigit():  # ✅ Validar que el ID sea un número válido
                return JsonResponse({'status': 'error', 'message': 'ID de clase no válido'}, status=400)

            clase = Clase.objects.get(id=int(clase_id))  # ✅ Convertir el ID a entero
            docente = Docente.objects.get(id=data['docente_id'])
            materia = Materia.objects.get(id=data['materia_id'])
            aula = Aula.objects.get(id=data['aula_id'])

            # Validar que hora_inicio sea menor que hora_fin
            if data['hora_inicio'] >= data['hora_fin']:
                return JsonResponse({'status': 'error', 'message': 'La hora de inicio debe ser menor que la hora de fin.'}, status=400)

            clase.docente = docente
            clase.materia = materia
            clase.aula = aula
            clase.hora_inicio = data['hora_inicio']
            clase.hora_fin = data['hora_fin']
            clase.fecha = data['fecha_inicio']
            clase.save()

            return JsonResponse({'status': 'success', 'message': 'Clase reprogramada'})
        except (Clase.DoesNotExist, Docente.DoesNotExist, Materia.DoesNotExist, Aula.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Clase, docente, materia o aula no encontrado'}, status=404)
        except Exception as e:
            print("Error al reprogramar la clase:", e)
            return JsonResponse({'status': 'error', 'message': 'Error interno del servidor'}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)
