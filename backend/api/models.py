from django.db import models
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.

class Usuarios(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    def __str__(self):
        return self.email
    
    def set_password(self, raw_password):
        """Encripta la contraseña usando la función de Django."""
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """Verifica si la contraseña ingresada coincide con la almacenada."""
        return check_password(raw_password, self.password)
    def has_perm(self, perm, obj=None):
        """El usuario tiene un permiso específico?"""
        return True

    def has_module_perms(self, app_label):
        """El usuario tiene permisos para ver una app específica?"""
        return True
# Modelo de eventos
class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_by = models.ForeignKey('Usuarios', on_delete=models.CASCADE, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

# Modelo de imágenes para eventos
class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='events/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.event.name}"

# Modelo de comentarios en eventos
class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('Usuarios', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('event', 'user')  # Un comentario único por usuario por evento

    def __str__(self):
        return f"Comment by {self.user.email} on {self.event.name}"    