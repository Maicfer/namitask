from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from .models import Actividad
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

from .models import ChecklistItem, Usuario, Tarea, Etiqueta, Adjunto, Actividad
from .serializers import (
    RegisterSerializer,
    UsuarioSerializer,
    PasswordChangeSerializer,
    TareaSerializer,
    EtiquetaSerializer,
    ChecklistItemSerializer,
    AdjuntoSerializer,
    ActividadSerializer
)

# ----------------------
# Registro
# ----------------------
class RegisterView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# ----------------------
# Perfil
# ----------------------
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# ----------------------
# Cambio de contraseña
# ----------------------
class CambiarPasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        if not user.check_password(old_password):
            return Response({"error": "La contraseña actual es incorrecta."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"success": "La contraseña se cambió correctamente."}, status=status.HTTP_200_OK)

# ----------------------
# Login personalizado con JWT
# ----------------------
class CustomLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email", "").strip().lower()
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email y contraseña son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"error": "Credenciales inválidas."}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "email": user.email,
                "nombre_completo": user.nombre_completo,
                "foto": user.foto.url if user.foto else None,
                "pais": user.pais,
                "ciudad": user.ciudad
            }
        })

# ----------------------
# Tareas
# ----------------------
class TareaViewSet(viewsets.ModelViewSet):
    serializer_class = TareaSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['estado', 'prioridad', 'asignado_a']
    ordering_fields = ['fecha_creacion', 'fecha_limite']
    search_fields = ['titulo', 'descripcion']

    def get_queryset(self):
        return Tarea.objects.filter(asignado_a=self.request.user)

    def perform_create(self, serializer):
        serializer.save(asignado_a=self.request.user)
        
    def perform_update(self, serializer):
        instance = serializer.save()
        Actividad.objects.create(
        tarea=instance,
        descripcion=f"La tarea fue actualizada por {self.request.user.nombre_completo}"
        )    

# ----------------------
# Etiquetas
# ----------------------
class EtiquetaViewSet(viewsets.ModelViewSet):
    queryset = Etiqueta.objects.all()
    serializer_class = EtiquetaSerializer
    permission_classes = [permissions.IsAuthenticated]

# ----------------------
# Checklist Items
# ----------------------
class ChecklistItemViewSet(viewsets.ModelViewSet):
    queryset = ChecklistItem.objects.all()
    serializer_class = ChecklistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

# ----------------------
# Adjuntos
# ----------------------
class AdjuntoViewSet(viewsets.ModelViewSet):
    queryset = Adjunto.objects.all()
    serializer_class = AdjuntoSerializer
    permission_classes = [permissions.IsAuthenticated]

# ----------------------
# Historial de Actividad
# ----------------------
class ActividadViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ActividadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        tarea_id = self.request.query_params.get('tarea')
        if tarea_id:
            return Actividad.objects.filter(tarea_id=tarea_id).order_by('-fecha')
        return Actividad.objects.none()





