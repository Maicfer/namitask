from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView,
    CambiarPasswordView,
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
router.register(r'checklist', ChecklistItemViewSet, basename='checklist')
router.register(r'adjuntos', AdjuntoViewSet, basename='adjunto')
router.register(r'actividades', ActividadViewSet, basename='actividad')

urlpatterns = [
    # Rutas para vista automática de la API (DRF Router)
    path('', include(router.urls)),
    
    # Rutas para las acciones personalizadas de TareaViewSet
    path('tareas/<int:pk>/completar_checklist_item/', TareaViewSet.as_view({'post': 'completar_checklist_item'}), name='tarea-completar-checklist-item'),
    path('tareas/<int:pk>/eliminar_adjunto/', TareaViewSet.as_view({'post': 'eliminar_adjunto'}), name='tarea-eliminar-adjunto'),

    # Rutas para autenticación y perfil
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/cambiar-clave/', CambiarPasswordView.as_view(), name='cambiar-clave'),

    # Rutas JWT
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]



