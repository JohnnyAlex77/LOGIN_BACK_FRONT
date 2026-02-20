"""
Django settings for login project.
"""

from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Esta clave se usa para firmar cookies, sesiones y tokens JWT.
# En producción, NUNCA debe estar en el código. Debe venir de variables de entorno.
SECRET_KEY = 'django-insecure-@n#o+o_l)x_9*=-b_4mj651d=u#awb*%i4g-3nx=mc=&i$62u^'

# SECURITY WARNING: don't run with debug turned on in production!
# Debug=True muestra trazas de error detalladas. Útil en desarrollo, peligroso en producción.
DEBUG = True

# Hosts/dominios permitidos para servir la aplicación.
# En producción, aquí iría el dominio real (ej: 'mipagina.com')
ALLOWED_HOSTS = ['localhost','127.0.0.1','0.0.0.0']

# Modelo de usuario personalizado
# Le decimos a Django que use nuestro modelo Usuario en lugar del predeterminado.
# Esto debe hacerse ANTES de la primera migración.
AUTH_USER_MODEL = 'usuarios.Usuario'

# Lista de aplicaciones instaladas.
# El orden puede importar (ej: las apps de terceros antes que las locales).
INSTALLED_APPS = [
    # Apps nativas de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',  # Django REST Framework
    'rest_framework_simplejwt',  # JWT authentication
    'rest_framework_simplejwt.token_blacklist',  # Para poder invalidar tokens (logout)
    'corsheaders',  # Para manejar CORS (permisos de frontend)
    
    # Local apps
    'usuarios',
    'estudiantes',
    'empresas',
   
]

# Middleware: componentes que procesan cada petición antes de llegar a la vista.
# El orden es importante: CorsMiddleware debe ir antes que CommonMiddleware.
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Maneja headers CORS
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de JWT (JSON Web Tokens)
# Usamos la librería simplejwt.
SIMPLE_JWT = {
    # Tiempo de vida del token de acceso (corto, por seguridad)
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    # Tiempo de vida del refresh token (más largo, para no pedir login cada rato)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    # Si es True, al refrescar el token se genera uno nuevo y el viejo se invalida
    'ROTATE_REFRESH_TOKENS': True,
    # Si es True, los tokens rotados se añaden a lista negra (requiere app token_blacklist)
    'BLACKLIST_AFTER_ROTATION': True,  # Para logout
    # Actualiza el campo last_login del usuario al obtener un nuevo token
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,  # Usamos la misma SECRET_KEY del proyecto
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    
    'AUTH_HEADER_TYPES': ('Bearer',),  # Header: Authorization: Bearer <token>
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',  # El campo del modelo User que se usará como ID
    'USER_ID_CLAIM': 'user_id',  # El nombre del claim en el token
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    
    'JTI_CLAIM': 'jti',  # Claim para ID único del token
    
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Configuración de CORS (Cross-Origin Resource Sharing)
# Permite que el frontend (React en puerto 5173) pueda hacer peticiones al backend.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Puerto de Vite
    "http://127.0.0.1:5173",
]

# Permite enviar cookies (como el refresh token HttpOnly) en peticiones cross-origin.
CORS_ALLOW_CREDENTIALS = True  # Para cookies HttpOnly

ROOT_URLCONF = 'login.urls'

# Configuración global de Django REST Framework
REST_FRAMEWORK = {
    # Clases de autenticación por defecto
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # Permisos por defecto: cualquier endpoint requiere autenticación
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # Solo devolvemos JSON, no HTML (típico de API)
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}

# Configuración de plantillas (no relevante para API, pero Django lo requiere)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'login.wsgi.application'


# Base de datos
# Usamos SQLite por simplicidad en desarrollo. En producción habría que cambiar.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Validación de contraseñas (recomendado mantenerlas en producción)
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'