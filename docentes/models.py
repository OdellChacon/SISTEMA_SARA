from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo electrónico es obligatorio')
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(correo, password, **extra_fields)

class BaseUser(AbstractUser):
    username = None  # Eliminar el campo username heredado
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=30)
    cedula = models.CharField(max_length=8, unique=True)
    activo = models.BooleanField(default=True)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido', 'telefono', 'cedula']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
rol = [
    (1, "Administrador"),
    (2, "Docente"),
]

class Docente(BaseUser):
    rol = models.IntegerField(choices=rol, default=2)

    class Meta:
        verbose_name = "Docente"
        verbose_name_plural = "Docentes"

class Administrador(BaseUser):
    rol = models.IntegerField(choices=rol, default=1)

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"