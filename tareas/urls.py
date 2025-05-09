from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import CustomTokenObtainPairView
from .views import CambiarPasswordView

from .views import (
    RegisterView,
    ProfileView,
    TareaViewSet,
    EtiquetaViewSet,
    ChecklistItemViewSet,
    AdjuntoViewSet,
    ActividadViewSet,
)

router = DefaultRouter()
router.register(r'tareas', TareaViewSet, basename='tarea')
router.register(r'etiquetas', EtiquetaViewSet, basename='etiqueta')
router.register(r'checklist', ChecklistItemViewSet)
router.register(r'adjuntos', AdjuntoViewSet, basename='adjunto')
router.register(r'actividad', ActividadViewSet, basename='actividad')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/cambiar-clave/', CambiarPasswordView.as_view(), name='cambiar-clave'),
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('cambiar-password/', CambiarPasswordView.as_view(), name='cambiar-password'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


