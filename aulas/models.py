from django.db import models

class Aula(models.Model):

    codigo_aula = models.CharField(max_length=30)  # Quitar unique=True
    descripcion = models.CharField(max_length=255, blank=True)
    capacidad = models.PositiveIntegerField()
    estatus = models.CharField(max_length=30)
    sede = models.CharField(max_length=50)
    serial = models.CharField(max_length=50, blank=True)


    def __str__(self):
        return f"{self.codigo_aula} - {self.descripcion}"
