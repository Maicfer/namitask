from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings

# -------------------------------
# MANAGER PERSONALIZADO DE USUARIO
# -------------------------------
class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre_completo, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, nombre_completo=nombre_completo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre_completo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, nombre_completo, password, **extra_fields)

# -------------------------------
# MODELO PERSONALIZADO DE USUARIO
# -------------------------------
class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre_completo, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, nombre_completo=nombre_completo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre_completo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, nombre_completo, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    GENERO_OPCIONES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    email = models.EmailField(unique=True)
    nombre_completo = models.CharField(max_length=100)
    celular = models.CharField(max_length=15, blank=True)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    pais = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    numero_documento = models.CharField(max_length=30, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=1, choices=GENERO_OPCIONES, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre_completo']

    def __str__(self):
        return self.email
# -------------------------------
# MODELO DE ETIQUETA
# -------------------------------
class Etiqueta(models.Model):
    nombre = models.CharField(max_length=50)
    color = models.CharField(max_length=20, default='gris')  # opcional: azul, rojo, etc.

    def __str__(self):
        return self.nombre

# -------------------------------
# MODELO DE TAREA
# -------------------------------
class Tarea(models.Model):
    ESTADO_OPCIONES = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('completada', 'Completada'),
    ]

    PRIORIDAD_OPCIONES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]

    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_OPCIONES, default='pendiente')
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_OPCIONES, default='media')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateField(null=True, blank=True)
    asignado_a = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tareas')
    etiquetas = models.ManyToManyField(Etiqueta, blank=True, related_name='tareas')

    def __str__(self):
        return self.titulo

# -------------------------------
# MODELO DE CHECKLIST
# -------------------------------
class ChecklistItem(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name="checklist_items")
    nombre = models.CharField(max_length=255)
    completado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {'✔️' if self.completado else '❌'}"
    
# -------------------------------
# MODELO DE ADJUNTO
# -------------------------------
class Adjunto(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='adjuntos')
    archivo = models.FileField(upload_to='adjuntos_tareas/')
    descripcion = models.CharField(max_length=255, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Adjunto para {self.tarea.titulo}"
# -------------------------------
# MODELO DE HISTORIAL ACTIVIDAD
# -------------------------------    
class Actividad(models.Model):
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name="actividades")
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tarea.titulo} - {self.descripcion[:30]}..."
    
