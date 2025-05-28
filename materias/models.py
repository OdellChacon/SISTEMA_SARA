from django.db import models

class Materia(models.Model):
    codigo_materia = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    trayecto = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.codigo_materia} - {self.descripcion}"
