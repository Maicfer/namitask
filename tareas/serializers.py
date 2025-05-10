from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Usuario, Tarea, Etiqueta, ChecklistItem, Adjunto, Actividad
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

# -------------------------
# SERIALIZADOR JWT CUSTOM
# -------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['nombre_completo'] = user.nombre_completo
        token['pais'] = user.pais
        token['ciudad'] = user.ciudad
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            "id": self.user.id,
            "email": self.user.email,
            "nombre_completo": self.user.nombre_completo,
            "foto": self.user.foto.url if self.user.foto else None,
            "pais": self.user.pais,
            "ciudad": self.user.ciudad
        }
        return data

# -------------------------
# SERIALIZADOR DE REGISTRO
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
# SERIALIZADOR DE PERFIL
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
# SERIALIZADOR DE HISTORIAL
# -------------------------
class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ['id', 'tarea', 'descripcion', 'fecha']
        read_only_fields = ['id', 'fecha']

# -------------------------
# SERIALIZADOR DE ADJUNTOS
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




