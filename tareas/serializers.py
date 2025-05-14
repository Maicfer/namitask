from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import Tarea, Etiqueta, ChecklistItem, Adjunto, Actividad

Usuario = get_user_model()

# -------------------------
# SERIALIZADOR JWT CUSTOM
# -------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['nombre'] = user.nombre_completo
        return token

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Usuario no encontrado")

        if not user.check_password(password):
            raise serializers.ValidationError("Contraseña incorrecta")

        data = super().validate({"username": user.email, "password": password})
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'nombre': user.nombre_completo,
        }
        return data

    def to_internal_value(self, data):
        data["username"] = data.get("email")
        return super().to_internal_value(data)


# -------------------------
# REGISTRO
# -------------------------
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Usuario.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = (
            'email', 'nombre_completo', 'password', 'password2',
            'numero_documento', 'fecha_nacimiento', 'pais', 'ciudad',
            'celular', 'genero'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        return Usuario.objects.create_user(**validated_data)

# -------------------------
# PERFIL
# -------------------------
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'email', 'nombre_completo', 'celular', 'foto', 'pais', 'ciudad')
        read_only_fields = ('id', 'email')

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

# -------------------------
# HISTORIAL
# -------------------------
class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ['id', 'tarea', 'descripcion', 'fecha']
        read_only_fields = ['id', 'fecha']

# -------------------------
# ADJUNTOS
# -------------------------
class AdjuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adjunto
        fields = ['id', 'archivo', 'descripcion', 'fecha_subida', 'tarea']
        read_only_fields = ['id', 'fecha_subida']

# -------------------------
# ETIQUETAS
# -------------------------
class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = ['id', 'nombre', 'color']

# -------------------------
# CHECKLIST
# -------------------------
class ChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = '__all__'
        read_only_fields = ['id', 'fecha_creacion']

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        tarea = instance.tarea
        items = tarea.checklist_items.all()
        if items.exists() and all(item.completado for item in items):
            tarea.estado = 'completada'
        else:
            tarea.estado = 'pendiente'
        tarea.save()
        return instance

# -------------------------
# TAREAS
# -------------------------
class TareaSerializer(serializers.ModelSerializer):
    checklist = ChecklistItemSerializer(many=True, read_only=True)
    etiquetas = EtiquetaSerializer(many=True, read_only=True)
    etiquetas_ids = serializers.PrimaryKeyRelatedField(
        queryset=Etiqueta.objects.all(), many=True, write_only=True, source='etiquetas'
    )

    class Meta:
        model = Tarea
        fields = [
            'id', 'titulo', 'descripcion', 'estado', 'prioridad',
            'fecha_creacion', 'fecha_limite', 'asignado_a',
            'etiquetas', 'etiquetas_ids', 'checklist'
        ]
        read_only_fields = ['asignado_a']

