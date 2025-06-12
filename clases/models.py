from django.db import models
from django.utils import timezone
from docentes.models import Docente
from aulas.models import Aula
from materias.models import Materia
from django.core.exceptions import ValidationError

def hora_actual():
    return timezone.now().time()

class Clase(models.Model):
    id = models.AutoField(primary_key=True)  # ID único generado automáticamente
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)  
    fecha = models.DateField(null=False, default=timezone.now)
    hora_inicio = models.TimeField(null=False)
    hora_fin = models.TimeField(null=False)
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE)  

    def __str__(self):
        return f"{self.materia} - {self.docente} ({self.hora_inicio} - {self.hora_fin})"

    def clean(self):
        # Verificar conflictos de horarios
        conflictos = Clase.objects.filter(
            aula=self.aula,
            fecha=self.fecha,
            hora_inicio__lt=self.hora_fin,
            hora_fin__gt=self.hora_inicio
        ).exclude(id=self.id)
        if conflictos.exists():
            raise ValidationError("Conflicto de horarios en el aula seleccionada.")


class Asistencia(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name="asistencias")
    foto_clase = models.ImageField(upload_to="asistencias/clase/")
    foto_lista = models.ImageField(upload_to="asistencias/lista/")
    foto_selfie = models.ImageField(upload_to="asistencias/selfies/")
    comentarios = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Asistencia de {self.clase.materia}"

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_fin = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.titulo

class Incumplimiento(models.Model):
    clase = models.ForeignKey(Clase, on_delete=models.CASCADE, related_name="incumplimientos")
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    fecha_reporte = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Incumplimiento de {self.docente.nombre} en {self.clase.materia}"
