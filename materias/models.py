from django.db import models

class Materia(models.Model):
    codigo_materia = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    carrera = models.CharField(max_length=100)      # Nuevo campo
    trayecto = models.CharField(max_length=50)      # Aumenta longitud si es necesario
    trimestre = models.CharField(max_length=10)     # Nuevo campo

    def __str__(self):
        return f"{self.codigo_materia} - {self.descripcion} ({self.carrera}, {self.trayecto}, Trim: {self.trimestre})"
