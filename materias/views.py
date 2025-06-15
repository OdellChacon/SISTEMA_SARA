from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.paginator import Paginator
import csv
import json
from .models import Materia
from .forms import MateriaForm


def materias_list(request):
    materias = Materia.objects.all().order_by('carrera', 'trayecto', 'codigo_materia')
    paginator = Paginator(materias, 5)  # Cambiado a 5 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'materias/materias_list.html', {'page_obj': page_obj, 'materias': page_obj.object_list})


def registrar_materia(request):
    if request.method == 'POST':
        form = MateriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('materias_list')
    else:
        form = MateriaForm()
    return render(request, 'materias/registrar_materia.html', {'form': form})


def editar_materia(request, materia_id):
    materia = get_object_or_404(Materia, id=materia_id)
    
    if request.method == 'POST':
        form = MateriaForm(request.POST, instance=materia)
        if form.is_valid():
            form.save()
            return redirect('materias_list')
    else:
        form = MateriaForm(instance=materia)
    
    return render(request, 'materias/editar_materia.html', {'form': form, 'materia': materia})


@csrf_exempt
def eliminar_materia(request, materia_id):
    if request.method == 'POST':
        materia = get_object_or_404(Materia, id=materia_id)
        try:
            materia.delete()
            return JsonResponse({'success': True, 'message': 'Materia eliminada correctamente.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)


@csrf_exempt
def importar_materias(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        reader = csv.reader(file.read().decode('utf-8').splitlines())
        header = next(reader)
        try:
            idx_codigo = header.index('codigo_materia')
            idx_desc = header.index('descripcion')
            idx_carrera = header.index('carrera')
            idx_trayecto = header.index('trayecto')
            idx_trimestre = header.index('trimestre')
        except ValueError:
            return JsonResponse({'success': False, 'message': 'El archivo debe tener las columnas: codigo_materia, descripcion, carrera, trayecto, trimestre'}, status=400)
        for row in reader:
            if len(row) <= max(idx_codigo, idx_desc, idx_carrera, idx_trayecto, idx_trimestre):
                continue
            Materia.objects.create(
                codigo_materia=row[idx_codigo],
                descripcion=row[idx_desc],
                carrera=row[idx_carrera],
                trayecto=row[idx_trayecto],
                trimestre=row[idx_trimestre]
            )
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Archivo no válido'}, status=400)


def exportar_materias(request, format, scope):
    materias = Materia.objects.all() if scope == "all" else Materia.objects.filter(id__in=scope.split(","))
    
    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="materias.csv"'
        writer = csv.writer(response)
        writer.writerow(['codigo_materia', 'descripcion', 'carrera', 'trayecto', 'trimestre'])
        for materia in materias:
            writer.writerow([materia.codigo_materia, materia.descripcion, materia.carrera, materia.trayecto, materia.trimestre])
        return response

    # Aquí puedes agregar soporte a otros formatos: json, xml, etc.
    return JsonResponse({'success': False, 'message': 'Formato no soportado'}, status=400)


@csrf_exempt
def eliminar_seleccionados(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ids = data.get('ids', [])
        Materia.objects.filter(id__in=ids).delete()
        return JsonResponse({'success': True, 'message': 'Registros eliminados correctamente.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)


def obtener_todos_los_ids(request):
    if request.method == 'GET':
        ids = list(Materia.objects.values_list('id', flat=True))
        return JsonResponse({'ids': ids})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def buscar_materias(request):
    query = request.GET.get('q', '').strip()
    page_number = request.GET.get('page', 1)
    if query:
        materias = Materia.objects.filter(
            codigo_materia__icontains=query
        ) | Materia.objects.filter(
            descripcion__icontains=query
        ) | Materia.objects.filter(
            trayecto__icontains=query
        ) | Materia.objects.filter(
            carrera__icontains=query
        ) | Materia.objects.filter(
            trimestre__icontains=query
        )
        materias = materias.order_by('carrera', 'trayecto', 'codigo_materia')
        paginator = Paginator(materias, 5)  # Limita a 5 resultados por página
        page_obj = paginator.get_page(page_number)
        results = [
            {
                'id': materia.id,
                'codigo_materia': materia.codigo_materia,
                'descripcion': materia.descripcion,
                'carrera': materia.carrera,
                'trayecto': materia.trayecto,
                'trimestre': materia.trimestre,
                # Agrega aquí otros campos si existen en el modelo Materia
                # 'otro_campo': materia.otro_campo,
            } for materia in page_obj
        ]
        response = {
            'results': results,
            'num_pages': paginator.num_pages,
            'current_page': page_obj.number,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
        }
    else:
        response = {
            'results': [],
            'num_pages': 0,
            'current_page': 1,
            'has_previous': False,
            'has_next': False,
        }
    return JsonResponse(response)
