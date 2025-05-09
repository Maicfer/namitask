from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Usuario, Tarea, Etiqueta, ChecklistItem, Adjunto, Actividad
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator

# -------------------------
# SERIALIZADOR JWT CUSTOM
# -------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

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
# RESTO SIN CAMBIOS...
# (ActividadSerializer, AdjuntoSerializer, EtiquetaSerializer, ChecklistItemSerializer, TareaSerializer)
# (no los repito porque no se tocaron)



