from rest_framework import serializers
from .models import *


# Crear y actualizar usuario
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = ['id', 'email', 'name', 'password', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Usuarios(
            email=validated_data['email'],
            name=validated_data['name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance


# Cambiar contraseña
class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


# Serializador para eventos
class EventSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='created_by.email')  # Mostrar el email del propietario

    class Meta:
        model = Event
        fields = '__all__'


# Serializador para imágenes de eventos
class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = '__all__'


# Serializador para comentarios
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')  # Mostrar el email del usuario

    class Meta:
        model = Comment
        exclude = ['is_deleted']  # Excluir el campo de eliminación lógica