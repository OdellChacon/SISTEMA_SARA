from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import csv
from .models import Aula
from .forms import AulaForm  # Asegúrate de tener un formulario para Aula
from django.core.paginator import Paginator
import json

def aulas_list(request):
    aulas = Aula.objects.all()
    paginator = Paginator(aulas, 5)  # Mostrar 5 registros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'aulas/aulas_list.html', {'page_obj': page_obj, 'aulas': page_obj.object_list})

def registrar_aula(request):
    if request.method == 'POST':
        form = AulaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('aulas_list')
    else:
        form = AulaForm()
    return render(request, 'aulas/registrar_aula.html', {'form': form})

def editar_aula(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    if request.method == 'POST':
        if 'eliminar' in request.POST:  # Manejar eliminación
            aula.delete()
            return JsonResponse({'success': True})
        form = AulaForm(request.POST, instance=aula)
        if form.is_valid():
            form.save()
            return redirect('aulas_list')
    else:
        form = AulaForm(instance=aula)
    return render(request, 'aulas/editar_aula.html', {'form': form, 'aula': aula})

@csrf_exempt
def eliminar_aula(request, aula_id):
    if request.method == 'POST':
        aula = get_object_or_404(Aula, id=aula_id)
        aula.delete()
        return JsonResponse({'success': True, 'message': 'Aula eliminada correctamente.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)

@csrf_exempt
def importar_aulas(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        reader = csv.reader(file.read().decode('utf-8').splitlines())
        next(reader)  # Saltar encabezado
        for row in reader:
            Aula.objects.create(departamento=row[0], tipo=row[1], numero=row[2])
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Archivo no válido'}, status=400)

def exportar_aulas(request, format, scope):
    aulas = Aula.objects.all() if scope == "all" else Aula.objects.filter(id__in=scope.split(","))
    
    if format == "csv":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="aulas.csv"'
        writer = csv.writer(response)
        writer.writerow(['Departamento', 'Tipo', 'Número'])
        for aula in aulas:
            writer.writerow([aula.departamento, aula.tipo, aula.numero])
        return response

    # Agregar lógica para otros formatos si es necesario
    return JsonResponse({'success': False, 'message': 'Formato no soportado'}, status=400)

@csrf_exempt
def eliminar_seleccionados(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ids = data.get('ids', [])
        Aula.objects.filter(id__in=ids).delete()
        return JsonResponse({'success': True, 'message': 'Registros eliminados correctamente.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)

def obtener_todos_los_ids(request):
    if request.method == 'GET':
        ids = list(Aula.objects.values_list('id', flat=True))
        return JsonResponse({'ids': ids})
    return JsonResponse({'error': 'Método no permitido'}, status=405)
