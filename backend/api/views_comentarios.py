from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from .models import *
from .serializer import *


# CRUD para comentarios
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Un usuario puede comentar solo una vez por evento."""
        event = serializer.validated_data['event']
        
        # Verificar si el usuario ya ha comentado en este evento
        comment = Comment.objects.filter(event=event, user=self.request.user).first()
        # Si ya existe un comentario, lanzar un ValidationError
        if comment:
            raise ValidationError("Ya has comentado este evento.")
        
        # Guardar el comentario si no existe
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        """Un usuario solo puede editar su propio comentario."""
        comment = self.get_object()
        if comment.user != request.user:
            return Response({'error': 'No tienes permiso para editar este comentario'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Un usuario solo puede eliminar su propio comentario (eliminación lógica)."""
        comment = self.get_object()
        if comment.user != request.user:
            return Response({'error': 'No tienes permiso para eliminar este comentario'}, status=status.HTTP_403_FORBIDDEN)
        comment.is_deleted = True
        comment.save()
        return Response({'detail': 'Comentario eliminado'}, status=status.HTTP_204_NO_CONTENT)