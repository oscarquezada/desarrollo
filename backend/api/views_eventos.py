from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import *
from .serializer import *



# CRUD para eventos
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Asociar el evento al usuario que lo crea."""
        serializer.save(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        """Permitir que solo el creador del evento edite los datos."""
        event = self.get_object()
        if event.created_by != request.user:
            return Response({'error': 'No tienes permiso para editar este evento'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Permitir que solo el creador del evento elimine el evento."""
        event = self.get_object()
        if event.created_by != request.user:
            return Response({'error': 'No tienes permiso para eliminar este evento'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


# CRUD para imágenes de eventos
class EventImageViewSet(viewsets.ModelViewSet):
    queryset = EventImage.objects.all()
    serializer_class = EventImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Permitir que solo el creador del evento suba imágenes."""
        event = serializer.validated_data['event']
        if event.created_by != self.request.user:
            raise PermissionError("No tienes permiso para agregar imágenes a este evento.")
        serializer.save()

    def update(self, request, *args, **kwargs):
        """Permitir que solo el creador del evento edite imágenes."""
        image = self.get_object()
        if image.event.created_by != request.user:
            return Response({'error': 'No tienes permiso para editar esta imagen'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Permitir que solo el creador del evento elimine imágenes."""
        image = self.get_object()
        if image.event.created_by != request.user:
            return Response({'error': 'No tienes permiso para eliminar esta imagen'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)