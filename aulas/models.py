from django.db import models

class Aula(models.Model):
    DEPARTAMENTO_CHOICES = [
        ('Agroalimentación', 'Agroalimentación'),
        ('Construcción Civil', 'Construcción Civil'),
        ('Electricidad', 'Electricidad'),
        ('Informática', 'Informática'),
        ('Ingeniería de Mantenimiento', 'Ingeniería de Mantenimiento'),
        ('Mecánica', 'Mecánica'),
        ('Procesamiento y Control de Alimentos', 'Procesamiento y Control de Alimentos'),
    ]
    TIPO_CHOICES = [
        ('Aula', 'Aula'),
        ('Laboratorio', 'Laboratorio'),
    ]

    departamento = models.CharField(max_length=50, choices=DEPARTAMENTO_CHOICES)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    numero = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.tipo} {self.numero} - {self.departamento}"
