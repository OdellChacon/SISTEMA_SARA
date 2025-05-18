from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.paginator import Paginator
import csv
import json
from .models import Materia
from .forms import MateriaForm


def materias_list(request):
    materias = Materia.objects.all()
    paginator = Paginator(materias, 5)
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
        next(reader)  # Saltar encabezado
        for row in reader:
            Materia.objects.create(nombre=row[0], codigo=row[1])
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Archivo no válido'}, status=400)


def exportar_materias(request, format, scope):
    materias = Materia.objects.all() if scope == "all" else Materia.objects.filter(id__in=scope.split(","))
    
    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="materias.csv"'
        writer = csv.writer(response)
        writer.writerow(['Nombre', 'Código'])
        for materia in materias:
            writer.writerow([materia.nombre, materia.codigo])
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
    if query:
        materias = Materia.objects.filter(nombre__icontains=query) | Materia.objects.filter(codigo__icontains(query))
        results = [{'id': materia.id, 'nombre': materia.nombre, 'codigo': materia.codigo} for materia in materias]
    else:
        results = []
    return JsonResponse({'results': results})
