from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_comentarios import *
from .views_eventos import *
from .views_usuarios import *

# Configuración del router
router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('events', EventViewSet, basename='event')
router.register('event-images', EventImageViewSet, basename='event-image')
router.register('comments', CommentViewSet, basename='comment')

urlpatterns = [
    # Login
    path('login/', LoginView.as_view({'post': 'create'}), name='login'),
    
    # Recuperación de contraseña
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetView.as_view(), name='password-reset-confirm'),  # Nuevo endpoint
    
    # Cambio de contraseña
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    
    # Rutas de los routers
    path('', include(router.urls)),
]
