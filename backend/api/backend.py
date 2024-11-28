from django.contrib.auth.backends import BaseBackend
from .models import Usuarios

class MyBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            # Buscar al usuario por el email
            user = Usuarios.objects.get(email=email)
            # Verificar si la contraseña es correcta
            if user.check_password(password) and user.is_active:
                return user
        except Usuarios.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return Usuarios.objects.get(pk=user_id)
        except Usuarios.DoesNotExist:
            return None
