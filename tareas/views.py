from rest_framework import generics, permissions, status, viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch

from .models import ChecklistItem, Usuario, Tarea, Etiqueta, Adjunto, Actividad
from .serializers import (
    RegisterSerializer,
    UsuarioSerializer,
    PasswordChangeSerializer,
    TareaSerializer,
    EtiquetaSerializer,
    ChecklistItemSerializer,
    AdjuntoSerializer,
    ActividadSerializer,
    CustomTokenObtainPairSerializer,
)

# ----------------------
# Registro
# ----------------------
class RegisterView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            print(f"Usuario creado: {user.email}")
            # Autenticar al usuario recién registrado para generar tokens
            token_obtain_serializer = CustomTokenObtainPairSerializer(data=request.data)
            if token_obtain_serializer.is_valid():
                tokens = token_obtain_serializer.validated_data
                return Response({
                    "message": "Usuario creado exitosamente.",
                    "tokens": tokens
                }, status=status.HTTP_201_CREATED)
            else:
                # Si falla la generación de tokens, devolvemos un error
                return Response(token_obtain_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------
# Perfil
# ----------------------
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Soporte para imagenes y formularios

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
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


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
        return Tarea.objects.filter(asignado_a=self.request.user).prefetch_related('checklist_items')

    def perform_create(self, serializer):
        serializer.save(asignado_a=self.request.user)
        Actividad.objects.create(
            tarea=serializer.instance,
            descripcion=f"La tarea fue creada por {self.request.user.nombre_completo}"
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        Actividad.objects.create(
            tarea=instance,
            descripcion=f"La tarea fue actualizada por {self.request.user.nombre_completo}"
        )

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj

    @action(detail=True, methods=['post'])
    def completar_checklist_item(self, request, pk=None):
        tarea = self.get_object()
        item_id = request.data.get('item_id')
        completado = request.data.get('completado')
        try:
            checklist_item = ChecklistItem.objects.get(pk=item_id, tarea=tarea)
            checklist_item.completado = completado
            checklist_item.save()
            Actividad.objects.create(
                tarea=tarea,
                descripcion=f"Se {'completó' if completado else 'reabrió'} el item del checklist: {checklist_item.nombre}"
            )
            # Lógica para actualizar el estado de la tarea
            tarea.refresh_from_db()
            tarea.estado = 'completada' if tarea.checklist_items.all().exists() and all(
                item.completado for item in tarea.checklist_items.all()) else 'pendiente'
            tarea.save()
            return Response({'status': 'success', 'message': 'Checklist item actualizado y actividad registrada.'})
        except ChecklistItem.DoesNotExist:
            return Response({'error': 'Checklist item no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def eliminar_adjunto(self, request, pk=None):
        tarea = self.get_object()
        adjunto_id = request.data.get('adjunto_id')
        try:
            adjunto = Adjunto.objects.get(pk=adjunto_id, tarea=tarea)
            # Usamos adjunto.archivo.name para obtener el nombre del archivo
            descripcion = f"Se eliminó el adjunto: {adjunto.archivo.name.split('/')[-1]}"
            try:
                # Aquí podrías agregar lógica para eliminar el archivo físico si es necesario
                # Ejemplo: import os; os.remove(adjunto.archivo.path)
                pass
            except Exception as e:
                print(f"Error al intentar eliminar el archivo físico: {e}")
                # Decide si quieres que falle la eliminación del adjunto por esto
                # o simplemente loguear el error. Por ahora, continuaremos.
                pass
            adjunto.delete()
            try:
                Actividad.objects.create(tarea=tarea, descripcion=descripcion)
            except Exception as e:
                print(f"Error al crear actividad de eliminación de adjunto: {e}")
                # Decide cómo manejar el fallo al crear la actividad.
                pass
            return Response({'status': 'success', 'message': 'Adjunto eliminado y actividad registrada.'})
        except Adjunto.DoesNotExist:
            return Response({'error': 'Adjunto no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error inesperado al eliminar adjunto: {e}")
            return Response({'error': 'Ocurrió un error al eliminar el adjunto en el servidor.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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