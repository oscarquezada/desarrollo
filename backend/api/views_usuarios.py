from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import  IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken,TokenError, AccessToken
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from .serializer import *

# Vista para el login 
class LoginView(viewsets.ViewSet):
    def create(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = Usuarios.objects.get(email=email)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        except Usuarios.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)


# CRUD para usuarios
class UserViewSet(viewsets.ModelViewSet):
    queryset = Usuarios.objects.all()
    serializer_class = UserSerializer

    # Solo usuarios autenticados pueden actualizar o eliminar su cuenta
    permission_classes = [IsAuthenticated]
    
    def partial_update(self, request, *args, **kwargs):
        """Actualizar parcialmente los datos del usuario autenticado."""
        try:
            user = request.user
            serializer = self.get_serializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Usuarios.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    def destroy(self, request, *args, **kwargs):
        try:

            """Eliminación lógica del usuario autenticado."""
            user = request.user
            user.is_active = False
            user.save()
            return Response({'detail': 'Cuenta eliminada'}, status=status.HTTP_204_NO_CONTENT)
        except Usuarios.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

# Vista para cambiar contraseña
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """Cambiar la contraseña del usuario autenticado."""
        try:
            user = request.user
            serializer = ChangePasswordSerializer(data=request.data)
            if serializer.is_valid():
                if user.check_password(serializer.data['current_password']):
                    user.set_password(serializer.data['new_password'])
                    user.save()
                    return Response({'detail': 'Contraseña actualizada con éxito'})
                return Response({'error': 'Contraseña actual incorrecta'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Usuarios.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

class PasswordResetRequestView(APIView):
    # Versión comentada (cómo debería ser con frontend)
    """
    def post(self, request):
        email = request.data.get('email')
        try:
            user = Usuarios.objects.get(email=email)
            
            # Generar un token único y seguro
            reset_token = RefreshToken.for_user(user).access_token
            
            # URL del frontend para gestionar el restablecimiento de contraseña
            reset_link = f"http://frontend-url.com/reset-password/{reset_token}/"
            
            # Enviar el enlace por correo electrónico
            send_mail(
                subject='Recuperación de contraseña',
                message=f'Usa este enlace para restablecer tu contraseña: {reset_link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
            
            return Response({'detail': 'Correo enviado para recuperación de contraseña'})
        except Usuarios.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    """
    
    # Versión funcional (para probar con Postman sin frontend)
    def post(self, request):
        """
        Esta implementación es solo para demostrar cómo funcionaría la lógica de recuperación 
        de contraseña sin un frontend. Aquí el enlace con el token se envía directamente en la 
        respuesta, lo cual no es seguro y no debe hacerse en producción.
        """
        email = request.data.get('email')
        try:
            user = Usuarios.objects.get(email=email)
            
            # Generar un token único y seguro
            reset_token = RefreshToken.for_user(user).access_token
            
            # En lugar de un enlace del frontend, se devuelve directamente el token en la respuesta
            reset_link = f"http://example.com/reset-password/{reset_token}/"
            
            # Enviar el enlace por correo electrónico
            send_mail(
                subject='Recuperación de contraseña (Demo)',
                message=f'Este es un enlace de prueba para restablecer tu contraseña: {reset_link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
            
            # Responder con el enlace para probarlo desde Postman
            return Response({
                'detail': 'Correo enviado para recuperación de contraseña (demo)',
                'reset_link': reset_link  # Esto es solo para demostración, no debe hacerse en producción
            })
        except Usuarios.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)



class PasswordResetView(APIView):
    def post(self, request):
        """
        Endpoint para restablecer la contraseña de un usuario.
        Este recibe el token y la nueva contraseña como datos.
        """
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        if not token or not new_password:
            return Response({'error': 'Token y nueva contraseña son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decodificar el token para obtener el ID del usuario
            decoded_data = AccessToken(token)
            user_id = decoded_data['user_id']
            
            # Buscar al usuario en la base de datos
            user = Usuarios.objects.get(id=user_id)
            
            # Establecer la nueva contraseña
            user.set_password(new_password)
            user.save()
            
            return Response({'detail': 'Contraseña actualizada con éxito'}, status=status.HTTP_200_OK)
        except TokenError:
            return Response({'error': 'Token inválido o expirado'}, status=status.HTTP_400_BAD_REQUEST)
        except Usuarios.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)
