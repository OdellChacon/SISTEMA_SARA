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
        ids_seleccionados = request.GET.getlist("ids[]")
        docentes = docentes.filter(id__in=ids_seleccionados)

    if formato == "csv":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=docentes.csv"
        writer = csv.DictWriter(response, fieldnames=["nombre", "apellido", "correo", "telefono", "fecha_ingreso", "cedula", "contraseña", "activo"])
        writer.writeheader()
        for docente in docentes:
            writer.writerow({
                "nombre": docente.nombre,
                "apellido": docente.apellido,
                "correo": docente.correo,
                "telefono": docente.telefono,
                "fecha_ingreso": docente.fecha_ingreso.strftime("%Y-%m-%d"),
                "cedula": docente.cedula,
                "contraseña": docente.contraseña,
                "activo": "true" if docente.activo else "false"
            })
        return response

    elif formato == "json":
        try:
            data = [
                {
                    "nombre": docente.nombre,
                    "apellido": docente.apellido,
                    "correo": docente.correo,
                    "telefono": docente.telefono,
                    "fecha_ingreso": docente.fecha_ingreso.strftime("%Y-%m-%d"),
                    "cedula": docente.cedula,
                    "contraseña": docente.contraseña,
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
            data = [["Nombre", "Apellido", "Correo", "Teléfono", "Fecha Ingreso", "Cédula", "Contraseña", "Activo"]]
            for docente in docentes:
                data.append([
                    docente.nombre,
                    docente.apellido,
                    docente.correo,
                    docente.telefono,
                    docente.fecha_ingreso.strftime("%Y-%m-%d"),
                    docente.cedula,
                    docente.contraseña,
                    "Sí" if docente.activo else "No"
                ])

            # Crear tabla
            table = Table(data, colWidths=[80, 80, 120, 80, 80, 60, 80, 40])
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

            # Ajustar la tabla en múltiples páginas si es necesario
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
        df = pd.DataFrame(list(docentes.values("nombre", "apellido", "correo", "telefono", "fecha_ingreso", "cedula", "contraseña", "activo")))
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = "attachment; filename=docentes.xlsx"
        df.to_excel(response, index=False)
        return response

    elif formato == "sql":
        response = HttpResponse(content_type="text/plain")
        response["Content-Disposition"] = "attachment; filename=docentes.sql"
        for docente in docentes:
            response.write(
                f"INSERT INTO docentes_docente (nombre, apellido, correo, telefono, fecha_ingreso, cedula, contraseña, activo) "
                f"VALUES ('{docente.nombre}', '{docente.apellido}', '{docente.correo}', '{docente.telefono}', "
                f"'{docente.fecha_ingreso}', '{docente.cedula}', '{docente.contraseña}', {docente.activo});\n"
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
            response.write(f"    <correo>{docente.correo}</correo>\n")
            response.write(f"    <telefono>{docente.telefono}</telefono>\n")
            response.write(f"    <fecha_ingreso>{docente.fecha_ingreso}</fecha_ingreso>\n")
            response.write(f"    <cedula>{docente.cedula}</cedula>\n")
            response.write(f"    <contraseña>{docente.contraseña}</contraseña>\n")
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
            ids = data.get("ids", [])
            if not ids:
                return JsonResponse({"success": False, "error": "No se seleccionaron registros."}, status=400)

            Docente.objects.filter(id__in=ids).delete()
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

        print(f"Archivo recibido: {file.name}")  # Para depuración

        try:
            nuevos, duplicados, errores = 0, 0, 0  # Contadores

            # 📌 CSV
            if file.name.endswith(".csv"):
                data = file.read().decode("utf-8")
                csv_reader = csv.DictReader(io.StringIO(data))

                expected_headers = {"nombre", "apellido", "correo", "telefono", "fecha_ingreso", "cedula", "contraseña", "activo"}
                if not expected_headers.issubset(set(csv_reader.fieldnames)):
                    messages.error(request, "Los encabezados del archivo CSV no coinciden con el formato esperado.")
                    return redirect("docentes_list")

                for row in csv_reader:
                    print(f"Procesando fila CSV: {row}")  # Depuración: Ver cada fila procesada
                    try:
                        # Verificar si ya existe un docente con el mismo correo
                        if Docente.objects.filter(correo=row["correo"]).exists() or Docente.objects.filter(cedula=row["cedula"]).exists():
                            duplicados += 1
                        else:
                            Docente.objects.create(
                                nombre=row["nombre"],
                                apellido=row["apellido"],
                                correo=row["correo"],
                                telefono=row["telefono"],
                                fecha_ingreso=row["fecha_ingreso"],
                                cedula=row["cedula"],
                                contraseña=row["contraseña"],
                                activo=row["activo"].lower() in ["true", "1", "yes"]
                            )
                            nuevos += 1
                    except Exception as e:
                        errores += 1
                        print(f"Error al procesar fila CSV: {row} - Error: {e}")  # Registrar errores en filas específicas

            # 📌 JSON
            elif file.name.endswith(".json"):
                try:
                    data = json.load(file)
                    if not isinstance(data, list):
                        messages.error(request, "El archivo JSON debe contener una lista de objetos.")
                        return redirect("docentes_list")

                    for row in data:
                        # Validar que todos los campos requeridos estén presentes
                        required_fields = {"nombre", "apellido", "correo", "telefono", "fecha_ingreso", "cedula", "contraseña", "activo"}
                        if not required_fields.issubset(row.keys()):
                            errores += 1
                            print(f"Error: Faltan campos requeridos en el registro: {row}")
                            continue

                        # Verificar duplicados
                        if Docente.objects.filter(correo=row["correo"]).exists() or Docente.objects.filter(cedula=row["cedula"]).exists():
                            duplicados += 1
                        else:
                            # Crear el docente
                            Docente.objects.create(
                                nombre=row["nombre"],
                                apellido=row["apellido"],
                                correo=row["correo"],
                                telefono=row["telefono"],
                                fecha_ingreso=row["fecha_ingreso"],
                                cedula=row["cedula"],
                                contraseña=row["contraseña"],
                                activo=row["activo"] in [True, "true", "1", "yes"]
                            )
                            nuevos += 1
                except json.JSONDecodeError as e:
                    messages.error(request, f"Error al leer el archivo JSON: {str(e)}")
                    return redirect("docentes_list")

            # 📌 XML
            elif file.name.endswith(".xml"):
                tree = ET.parse(file)
                root = tree.getroot()

                for docente in root.findall("docente"):
                    datos = {
                        "nombre": docente.find("nombre").text.strip(),
                        "apellido": docente.find("apellido").text.strip(),
                        "correo": docente.find("correo").text.strip(),
                        "telefono": docente.find("telefono").text.strip(),
                        "fecha_ingreso": docente.find("fecha_ingreso").text.strip(),
                        "cedula": docente.find("cedula").text.strip(),
                        "contraseña": docente.find("contraseña").text.strip(),
                        "activo": docente.find("activo").text.strip().lower() in ["true", "1", "yes"]
                    }
                    if Docente.objects.filter(correo=datos["correo"]).exists() or Docente.objects.filter(cedula=datos["cedula"]).exists():
                        duplicados += 1
                    else:
                        Docente.objects.create(**datos)
                        nuevos += 1

            # 📌 EXCEL
            elif file.name.endswith(".xlsx"):
                df = pd.read_excel(file)
                expected_headers = {"nombre", "apellido", "correo", "telefono", "fecha_ingreso", "cedula", "contraseña", "activo"}
                if not expected_headers.issubset(set(df.columns)):
                    messages.error(request, "Los encabezados del archivo Excel no coinciden con el formato esperado.")
                    return redirect("docentes_list")

                for _, row in df.iterrows():
                    if Docente.objects.filter(correo=row["correo"]).exists() or Docente.objects.filter(cedula=row["cedula"]).exists():
                        duplicados += 1
                    else:
                        activo_valor = str(row["activo"]).strip().lower()
                        activo_convertido = activo_valor in ["true", "1", "yes", "sí"]

                        Docente.objects.create(
                            nombre=row["nombre"],
                            apellido=row["apellido"],
                            correo=row["correo"],
                            telefono=str(row["telefono"]),
                            fecha_ingreso=row["fecha_ingreso"],
                            cedula=row["cedula"],
                            contraseña=row["contraseña"],
                            activo=activo_convertido
                        )
                        nuevos += 1

            # 📌 SQL
            elif file.name.endswith(".sql"):
                sql_content = file.read().decode("utf-8").split("\n")
                for line in sql_content:
                    if "INSERT INTO" in line:
                        values_part = line.split("VALUES")[1].strip().strip(";").strip("()")
                        values = [v.strip("'") for v in values_part.split(", ")]

                        if len(values) == 8:
                            nombre, apellido, correo, telefono, fecha_ingreso, cedula, contraseña, activo = values
                            activo_convertido = activo.lower() in ["true", "1", "yes"]
                            if Docente.objects.filter(correo=correo).exists() or Docente.objects.filter(cedula=cedula).exists():
                                duplicados += 1
                            else:
                                Docente.objects.create(
                                    nombre=nombre,
                                    apellido=apellido,
                                    correo=correo,
                                    telefono=telefono,
                                    fecha_ingreso=fecha_ingreso,
                                    cedula=cedula,
                                    contraseña=contraseña,
                                    activo=activo_convertido
                                )
                                nuevos += 1

            # 📌 PDF
            elif file.name.endswith(".pdf"):
                try:
                    import pdfplumber
                    from datetime import datetime  

                    def convertir_fecha(fecha_str):
                        """Intenta convertir varias formas de fechas al formato YYYY-MM-DD."""
                        formatos = ["%d/%m/%Y", "%d-%m-%Y", "%m/%d/%Y", "%m-%d-%Y", "%Y/%m/%d", "%Y-%m-%d"]
                        for fmt in formatos:
                            try:
                                return datetime.strptime(fecha_str, fmt).strftime("%Y-%m-%d")
                            except ValueError:
                                continue
                        return None  

                    def convertir_activo(valor):
                        """Convierte el campo activo a True o False."""
                        valor = valor.strip().lower()  # Limpiar espacios y convertir a minúsculas
                        return valor in ["true", "1", "yes", "sí", "activo"]

                    def limpiar_fila(fila):
                        """Limpia y separa los datos de una fila."""
                        partes = fila.split()
                        if len(partes) < 8:
                            return None  # Fila inválida
                        return {
                            "nombre": partes[0],
                            "apellido": partes[1],
                            "correo": partes[2],
                            "telefono": partes[3],
                            "fecha_ingreso": partes[4],
                            "cedula": partes[5][:8],  # Truncar a 8 caracteres
                            "contraseña": partes[6],
                            "activo": partes[7]
                        }

                    full_text = ""
                    with pdfplumber.open(file) as pdf:
                        for page in pdf.pages:
                            extracted_text = page.extract_text()
                            if extracted_text:
                                full_text += extracted_text + "\n"

                    print(f"Texto extraído del PDF:\n{full_text}")  # Para depuración

                    lines = full_text.strip().split("\n")
                    if len(lines) < 2:
                        messages.error(request, "El archivo PDF no contiene datos suficientes para importar.")
                        return redirect("docentes_list")

                    headers = ["nombre", "apellido", "correo", "telefono", "fecha_ingreso", "cedula", "contraseña", "activo"]
                    data_rows = lines[1:]  # Omitir encabezados

                    for row in data_rows:
                        datos = limpiar_fila(row)
                        if not datos:
                            print(f"❌ Fila inválida: {row}")
                            errores += 1
                            continue

                        # Validar y convertir los datos
                        try:
                            fecha_ingreso = convertir_fecha(datos["fecha_ingreso"])
                            if not fecha_ingreso:
                                print(f"❌ Fecha inválida: {datos['fecha_ingreso']}")
                                errores += 1
                                continue

                            activo = convertir_activo(datos["activo"])

                            # Verificar duplicados
                            if Docente.objects.filter(correo=datos["correo"]).exists() or Docente.objects.filter(cedula=datos["cedula"]).exists():
                                duplicados += 1
                            else:
                                Docente.objects.create(
                                    nombre=datos["nombre"],
                                    apellido=datos["apellido"],
                                    correo=datos["correo"],
                                    telefono=datos["telefono"],
                                    fecha_ingreso=fecha_ingreso,
                                    cedula=datos["cedula"],
                                    contraseña=datos["contraseña"],
                                    activo=activo
                                )
                                nuevos += 1
                        except Exception as e:
                            print(f"Error al procesar fila: {row} - Error: {e}")
                            errores += 1

                    messages.success(request, f"{nuevos} docentes importados con éxito. {duplicados} duplicados omitidos.")
                    if errores > 0:
                        messages.error(request, f"{errores} registros no se pudieron procesar debido a errores.")
                    return redirect("docentes_list")

                except Exception as e:
                    print(f"Error al procesar el PDF: {e}")
                    messages.error(request, f"Ocurrió un error al procesar el archivo PDF: {str(e)}")
                    return redirect("docentes_list")

            else:
                messages.error(request, "Formato de archivo no soportado. Use CSV, JSON, XML, SQL, PDF o Excel.")
                return redirect("docentes_list")

            # Mensajes de éxito o advertencias
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
        ids = list(Docente.objects.values_list("id", flat=True))  # Obtener todos los IDs
        return JsonResponse({"ids": ids})
    return JsonResponse({"error": "Método no permitido."}, status=405)

@require_POST
@csrf_exempt
def eliminar_seleccionados_docentes(request):
    try:
        data = json.loads(request.body)
        ids = data.get("ids", [])
        if not ids:
            return JsonResponse({"success": False, "error": "No se seleccionaron registros."}, status=400)

        Docente.objects.filter(id__in=ids).delete()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


def detalle_docente(request, docente_id):
    docente = get_object_or_404(Docente, id=docente_id, rol=2)  # Filtrar por rol
    return render(request, 'docentes/detalle_docente.html', {'docente': docente})


def buscar_docentes(request):
    termino = request.GET.get('q', '').strip()
    if termino:
        docentes = Docente.buscar_por_termino(termino)
        resultados = [
            {
                'id': docente.id,
                'nombre': docente.nombre,
                'apellido': docente.apellido,
                'correo': docente.correo,
                'fecha_ingreso': docente.fecha_ingreso.strftime('%Y-%m-%d'),
                'activo': docente.activo,
            }
            for docente in docentes
        ]
        return JsonResponse({'results': resultados})
    return JsonResponse({'results': []})