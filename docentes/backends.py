from django.contrib.auth.backends import ModelBackend
from docentes.models import BaseUser

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Intentar autenticar por cedula
            user = BaseUser.objects.get(cedula=username)
        except BaseUser.DoesNotExist:
            return None

        # Verificar la contraseña y si el usuario está activo
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None