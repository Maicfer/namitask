from corsheaders.defaults import default_headers 
import os
from pathlib import Path
from datetime import timedelta
import dj_database_url



BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 Clave secreta
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-secret-key')

# 🛠️ Modo debug
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# 🌍 Dominios permitidos
ALLOWED_HOSTS = ['*']  # Puedes restringir en producción si deseas

# 🌐 CORS para frontend
CORS_ALLOWED_ORIGINS = [
    "https://namitask-frontend.onrender.com",
    "http://localhost:5173",
]
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    'content-type',
    'authorization',
    'x-csrftoken',
    'x-requested-with',
]

# 📦 Apps instaladas
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'tareas',
    'rest_framework_simplejwt',
    'django_filters',
]

# 🧱 Middleware
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para servir archivos estáticos en producción
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# 🖼️ Media (uploads de perfil, adjuntos)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 🎨 Plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# 🗃️ Base de datos
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:Travel@localhost:5432/namitask_db',
        conn_max_age=600,
    )
}
# 🔐 Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🔐 DRF y JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# 🧠 Usuario personalizado
AUTH_USER_MODEL = 'tareas.Usuario'

# ⚙️ Idioma y zona horaria
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


# 📁 Archivos estáticos (Render)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# 🏷️ Default ID field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
