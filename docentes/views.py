import json  # Asegúrate de importar json
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from .models import Docente, Administrador  # Importar los modelos actualizados
from .forms import *
from django.contrib import messages
import pandas as pd
import csv
import io
import xml.etree.ElementTree as ET
from PyPDF2 import PdfReader
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import pdfplumber
from django.core.paginator import Paginator  # Importar Paginator
from django.views.decorators.http import require_POST  # Importar require_POST


def docentes_list(request):
    docentes = Docente.objects.filter(rol=2).order_by('id')  # Filtrar solo docentes
    paginator = Paginator(docentes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'docentes/docentes_list.html', {
        'page_obj': page_obj,
        'docentes': page_obj.object_list,
    })


def registrar_docente(request):
    if request.method == 'POST':
        form = DocenteForm(request.POST)
        if form.is_valid():
            docente = form.save(commit=False)
            docente.rol = 2  # Asignar rol de docente
            # No asignar username, ya no existe
            docente.save()
            return redirect('docentes_list')
        else:
            print(form.errors)  # Para depuración, muestra errores en consola
    else:
        form = DocenteForm()

    return render(request, 'docentes/registrar_docente.html', {'form': form})


def editar_docente(request, docente_id):
    docente = get_object_or_404(Docente, id=docente_id, rol=2)  # Filtrar por rol

    if request.method == 'POST':
        form = DocenteUpdateForm(request.POST, instance=docente)
        if form.is_valid():
            form.save()
            return redirect('docentes_list')
    else:
        form = DocenteUpdateForm(instance=docente)

    return render(request, 'docentes/editar_docente.html', {'form': form, 'docente': docente})


@csrf_exempt  # ⚠️ Solo para pruebas, lo mejor es usar CSRF Token correctamente
def eliminar_docente(request, docente_id):
    if request.method == "POST":
        docente = get_object_or_404(Docente, id=docente_id, rol=2)  # Filtrar por rol
        docente.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

#ADMINISTRADORES
def admin_list(request):
    docentes = Administrador.objects.filter(rol=1).order_by('id')  # Filtrar solo docentes
    paginator = Paginator(docentes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'administradores/admin_list.html', {
        'page_obj': page_obj,
        'docentes': page_obj.object_list,
    })

def registrar_admin(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            docente = form.save(commit=False)
            docente.rol = 1  # Asignar rol de administrador
            # No asignar username, ya no existe
            docente.save()
            return redirect('admin_list')
    else:
        form = AdminForm()

    return render(request, 'administradores/registrar_admin.html', {'form': form})


def editar_admin(request, docente_id):
    docente = get_object_or_404(Administrador, id=docente_id, rol=2)  # Filtrar por rol

    if request.method == 'POST':
        form = AdminUpdateForm(request.POST, instance=docente)
        if form.is_valid():
            form.save()
            return redirect('admin_list')
    else:
        form = AdminUpdateForm(instance=docente)

    return render(request, 'administradores/editar_admin.html', {'form': form, 'docente': docente})


@csrf_exempt  # ⚠️ Solo para pruebas, lo mejor es usar CSRF Token correctamente
def eliminar_admin(request, docente_id):
    if request.method == "POST":
        docente = get_object_or_404(Administrador, id=docente_id, rol=1)  # Filtrar por rol
        docente.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

def detalle_admin(request, docente_id):
    docente = get_object_or_404(Administrador, id=docente_id, rol=2)  # Filtrar por rol
    return render(request, 'administrador/detalle_admin.html', {'docente': docente})


def exportar_docentes(request, formato, tipo):
    docentes = Docente.objects.all()

    if tipo == "selected":
        cedulas_seleccionadas = request.GET.getlist("cedulas[]")
        docentes = docentes.filter(cedula__in=cedulas_seleccionadas)

    if formato == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=docentes.csv"
        writer = csv.DictWriter(response, fieldnames=["nombre", "apellido", "cedula", "activo"])
        writer.writeheader()
        for docente in docentes:
            writer.writerow({
                "nombre": docente.nombre,
                "apellido": docente.apellido,
                "cedula": docente.cedula,
                "activo": "true" if docente.activo else "false"
            })
        return response

    elif formato == "json":
        try:
            data = [
                {
                    "nombre": docente.nombre,
                    "apellido": docente.apellido,
                    "cedula": docente.cedula,
                    "activo": docente.activo
                }
                for docente in docentes
            ]
            response = HttpResponse(json.dumps(data, indent=4), content_type="application/json")
            response["Content-Disposition"] = "attachment; filename=docentes.json"
            return response
        except Exception as e:
            messages.error(request, f"Error al exportar en JSON: {str(e)}")
            return redirect("docentes_list")

    elif formato == "pdf":
        try:
            buffer = BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter

            pdf.setTitle("Lista de Docentes")
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(200, height - 40, "Lista de Docentes")

            # Datos para la tabla
            data = [["Nombre", "Apellido", "Cédula", "Activo"]]
            for docente in docentes:
                data.append([
                    docente.nombre,
                    docente.apellido,
                    docente.cedula,
                    "Sí" if docente.activo else "No"
                ])

            table = Table(data, colWidths=[100, 100, 100, 60])
            style = TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ])
            table.setStyle(style)
            table.wrapOn(pdf, width, height)
            table.drawOn(pdf, 30, height - 200)

            pdf.save()
            buffer.seek(0)

            response = HttpResponse(buffer, content_type="application/pdf")
            response["Content-Disposition"] = 'attachment; filename="docentes.pdf"'
            return response
        except Exception as e:
            messages.error(request, f"Error al generar el PDF: {str(e)}")
            return redirect("docentes_list")

    elif formato == "excel":
        df = pd.DataFrame(list(docentes.values("nombre", "apellido", "cedula", "activo")))
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = "attachment; filename=docentes.xlsx"
        df.to_excel(response, index=False)
        return response

    elif formato == "sql":
        response = HttpResponse(content_type="text/plain")
        response["Content-Disposition"] = "attachment; filename=docentes.sql"
        for docente in docentes:
            response.write(
                f"INSERT INTO docentes_docente (nombre, apellido, cedula, activo) "
                f"VALUES ('{docente.nombre}', '{docente.apellido}', '{docente.cedula}', {docente.activo});\n"
            )
        return response

    elif formato == "xml":
        response = HttpResponse(content_type="application/xml")
        response["Content-Disposition"] = "attachment; filename=docentes.xml"
        response.write("<docentes>\n")
        for docente in docentes:
            response.write(f"  <docente>\n")
            response.write(f"    <nombre>{docente.nombre}</nombre>\n")
            response.write(f"    <apellido>{docente.apellido}</apellido>\n")
            response.write(f"    <cedula>{docente.cedula}</cedula>\n")
            response.write(f"    <activo>{docente.activo}</activo>\n")
            response.write(f"  </docente>\n")
        response.write("</docentes>")
        return response

    return HttpResponse("Formato no soportado", status=400)


@csrf_exempt
def eliminar_seleccionados(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            cedulas = data.get("cedulas", [])
            if not cedulas:
                return JsonResponse({"success": False, "error": "No se seleccionaron registros."}, status=400)
            Docente.objects.filter(cedula__in=cedulas).delete()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"success": False, "error": "Método no permitido."}, status=405)

def cargar_docentes(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        if not file:
            messages.error(request, "No se seleccionó ningún archivo.")
            return redirect("docentes_list")
        try:
            nuevos, duplicados, errores = 0, 0, 0
            # CSV
            if file.name.endswith(".csv"):
                data = file.read().decode("utf-8")
                csv_reader = csv.DictReader(io.StringIO(data))
                expected_headers = {"nombre", "apellido", "cedula", "activo"}
                alt_headers = {"cedula_docente", "apellidos", "nombres", "status"}
                fieldnames_set = set(csv_reader.fieldnames)
                if expected_headers.issubset(fieldnames_set):
                    for row in csv_reader:
                        try:
                            if Docente.objects.filter(cedula=row["cedula"]).exists():
                                duplicados += 1
                            else:
                                Docente.objects.create(
                                    nombre=row["nombre"],
                                    apellido=row["apellido"],
                                    cedula=row["cedula"],
                                    activo=row["activo"].lower() in ["true", "1", "yes", "activo"]
                                )
                                nuevos += 1
                        except Exception as e:
                            errores += 1
                elif alt_headers.issubset(fieldnames_set):
                    for row in csv_reader:
                        try:
                            cedula = row.get("cedula_docente", "").strip()
                            apellido = row.get("apellidos", "").strip()
                            nombre = row.get("nombres", "").strip()
                            status = row.get("status", "").strip().lower()
                            activo = status in ["activo", "active", "true", "1", "yes", "sí"]
                            if Docente.objects.filter(cedula=cedula).exists():
                                duplicados += 1
                            else:
                                Docente.objects.create(
                                    nombre=nombre,
                                    apellido=apellido,
                                    cedula=cedula,
                                    activo=activo
                                )
                                nuevos += 1
                        except Exception as e:
                            errores += 1
                else:
                    messages.error(request, "Los encabezados del archivo CSV no coinciden con el formato esperado.")
                    return redirect("docentes_list")
            # JSON
            elif file.name.endswith(".json"):
                try:
                    data = json.load(file)
                    if not isinstance(data, list):
                        messages.error(request, "El archivo JSON debe contener una lista de objetos.")
                        return redirect("docentes_list")
                    for row in data:
                        required_fields = {"nombre", "apellido", "cedula", "activo"}
                        if not required_fields.issubset(row.keys()):
                            errores += 1
                            continue
                        if Docente.objects.filter(cedula=row["cedula"]).exists():
                            duplicados += 1
                        else:
                            Docente.objects.create(
                                nombre=row["nombre"],
                                apellido=row["apellido"],
                                cedula=row["cedula"],
                                activo=row["activo"] in [True, "true", "1", "yes"]
                            )
                            nuevos += 1
                except json.JSONDecodeError as e:
                    messages.error(request, f"Error al leer el archivo JSON: {str(e)}")
                    return redirect("docentes_list")
            # XML
            elif file.name.endswith(".xml"):
                tree = ET.parse(file)
                root = tree.getroot()
                for docente in root.findall("docente"):
                    datos = {
                        "nombre": docente.find("nombre").text.strip(),
                        "apellido": docente.find("apellido").text.strip(),
                        "cedula": docente.find("cedula").text.strip(),
                        "activo": docente.find("activo").text.strip().lower() in ["true", "1", "yes"]
                    }
                    if Docente.objects.filter(cedula=datos["cedula"]).exists():
                        duplicados += 1
                    else:
                        Docente.objects.create(**datos)
                        nuevos += 1
            # EXCEL
            elif file.name.endswith(".xlsx"):
                df = pd.read_excel(file)
                expected_headers = {"nombre", "apellido", "cedula", "activo"}
                if not expected_headers.issubset(set(df.columns)):
                    messages.error(request, "Los encabezados del archivo Excel no coinciden con el formato esperado.")
                    return redirect("docentes_list")
                for _, row in df.iterrows():
                    if Docente.objects.filter(cedula=row["cedula"]).exists():
                        duplicados += 1
                    else:
                        activo_valor = str(row["activo"]).strip().lower()
                        activo_convertido = activo_valor in ["true", "1", "yes", "sí"]
                        Docente.objects.create(
                            nombre=row["nombre"],
                            apellido=row["apellido"],
                            cedula=row["cedula"],
                            activo=activo_convertido
                        )
                        nuevos += 1
            # SQL
            elif file.name.endswith(".sql"):
                sql_content = file.read().decode("utf-8").split("\n")
                for line in sql_content:
                    if "INSERT INTO" in line:
                        values_part = line.split("VALUES")[1].strip().strip(";").strip("()")
                        values = [v.strip("'") for v in values_part.split(", ")]
                        if len(values) == 4:
                            nombre, apellido, cedula, activo = values
                            activo_convertido = activo.lower() in ["true", "1", "yes"]
                            if Docente.objects.filter(cedula=cedula).exists():
                                duplicados += 1
                            else:
                                Docente.objects.create(
                                    nombre=nombre,
                                    apellido=apellido,
                                    cedula=cedula,
                                    activo=activo_convertido
                                )
                                nuevos += 1
            # PDF y otros formatos: omitir o adaptar si es necesario
            # ...existing code for PDF, adapt si quieres...
            # ...existing code...
            if nuevos > 0:
                messages.success(request, f"Se añadieron {nuevos} nuevos docentes.")
            if duplicados > 0:
                messages.warning(request, f"{duplicados} registros duplicados no fueron añadidos.")
            if errores > 0:
                messages.error(request, f"{errores} registros no se pudieron procesar debido a errores.")
        except Exception as e:
            messages.error(request, f"Error al procesar el archivo: {str(e)}")
        return redirect("docentes_list")

def obtener_todos_los_ids_docentes(request):
    if request.method == "GET":
        cedulas = list(Docente.objects.values_list("cedula", flat=True))
        return JsonResponse({"cedulas": cedulas})
    return JsonResponse({"error": "Método no permitido."}, status=405)

@require_POST
@csrf_exempt
def eliminar_seleccionados_docentes(request):
    try:
        data = json.loads(request.body)
        cedulas = data.get("cedulas", [])
        if not cedulas:
            return JsonResponse({"success": False, "error": "No se seleccionaron registros."}, status=400)
        Docente.objects.filter(cedula__in=cedulas).delete()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


def detalle_docente(request, docente_id):
    docente = get_object_or_404(Docente, id=docente_id, rol=2)  # Filtrar por rol
    return render(request, 'docentes/detalle_docente.html', {'docente': docente})


def buscar_docentes(request):
    termino = request.GET.get('q', '').strip()
    if termino:
        docentes = Docente.objects.filter(
            models.Q(nombre__icontains=termino) |
            models.Q(apellido__icontains=termino) |
            models.Q(cedula__icontains=termino)
        )
        resultados = [
            {
                'id': docente.id,
                'nombre': docente.nombre,
                'apellido': docente.apellido,
                'cedula': docente.cedula,
                'activo': docente.activo,
            }
            for docente in docentes
        ]
        return JsonResponse({'results': resultados})
    return JsonResponse({'results': []})