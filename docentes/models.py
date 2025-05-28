from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, cedula, password=None, **extra_fields):
        if not cedula:
            raise ValueError('La cédula es obligatoria')
        user = self.model(cedula=cedula, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cedula, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(cedula, password, **extra_fields)

class BaseUser(AbstractUser):
    nombre = models.CharField(max_length=100)      # nombres
    apellido = models.CharField(max_length=100)    # apellidos
    cedula = models.CharField(max_length=12, unique=True)  # cedula_docente
    activo = models.BooleanField(default=True)     # status

    USERNAME_FIELD = 'cedula'  # Cambiar a cedula para login por cédula
    REQUIRED_FIELDS = ['nombre', 'apellido']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        # Asegura que username siempre tenga un valor (por ejemplo, la cédula)
        if not self.username:
            self.username = self.cedula
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def set_status(self, status):
        self.activo = True if status == "Activo" else False
    
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