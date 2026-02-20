"""
Django settings for login project.
"""

from pathlib import Path
from datetime import timedelta

# =============================================================================
# RUTAS BASE DEL PROYECTO
# =============================================================================
# Construye rutas absolutas dentro del proyecto. BASE_DIR es la raíz del proyecto
# (la carpeta que contiene manage.py). Se usa como referencia para otras rutas.
BASE_DIR = Path(__file__).resolve().parent.parent


# =============================================================================
# CONFIGURACIÓN DE SEGURIDAD (PRODUCCIÓN)
# =============================================================================
# SECURITY WARNING: mantén la clave secreta en producción... ¡secreta!
# Esta clave se usa para firmar cookies, sesiones y tokens JWT.
# En producción, NUNCA debe estar en el código. Debe venir de variables de entorno.
SECRET_KEY = 'django-insecure-@n#o+o_l)x_9*=-b_4mj651d=u#awb*%i4g-3nx=mc=&i$62u^'

# SECURITY WARNING: no ejecutes con debug activado en producción.
# Debug=True muestra trazas de error detalladas. Útil en desarrollo, peligroso en producción.
DEBUG = True

# Hosts/dominios permitidos para servir la aplicación.
# En producción, aquí iría el dominio real (ej: 'mipagina.com')
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']


# =============================================================================
# MODELO DE USUARIO PERSONALIZADO
# =============================================================================
# Le decimos a Django que use nuestro modelo Usuario en lugar del predeterminado.
# Esto debe hacerse ANTES de la primera migración. Si se cambia después, es muy
# complicado migrar la base de datos.
AUTH_USER_MODEL = 'usuarios.Usuario'


# =============================================================================
# APLICACIONES INSTALADAS
# =============================================================================
# El orden puede importar: Django procesa las apps en este orden para plantillas,
# migraciones, etc. Es buena práctica poner apps de terceros antes que las locales.
INSTALLED_APPS = [
    # Apps nativas de Django (core del framework)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps (dependencias externas)
    'rest_framework',                          # Django REST Framework
    'rest_framework_simplejwt',                 # JWT authentication
    'rest_framework_simplejwt.token_blacklist', # Para poder invalidar tokens (logout)
    'corsheaders',                               # Para manejar CORS (permisos de frontend)
    
    # Local apps (nuestras aplicaciones)
    'usuarios',
    'estudiantes',
    'empresas',
]


# =============================================================================
# MIDDLEWARE
# =============================================================================
# Componentes que procesan cada petición HTTP antes de llegar a la vista.
# El orden es CRÍTICO: cada middleware puede modificar la petición o respuesta,
# y algunos dependen de otros. CorsMiddleware debe ir antes que CommonMiddleware.
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',    # Maneja headers CORS
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =============================================================================
# CONFIGURACIÓN DE URLs
# =============================================================================
# Archivo principal de rutas del proyecto
ROOT_URLCONF = 'login.urls'


# =============================================================================
# CONFIGURACIÓN DE PLANTILLAS
# =============================================================================
# No es muy relevante para una API, pero Django lo requiere.
# Define cómo Django busca y renderiza plantillas HTML.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],                              # Directorios adicionales de plantillas
        'APP_DIRS': True,                         # Buscar en carpetas 'templates' de cada app
        'OPTIONS': {
            'context_processors': [                # Variables disponibles en todas las plantillas
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# =============================================================================
# CONFIGURACIÓN WSGI
# =============================================================================
# Punto de entrada para servidores WSGI compatibles (Gunicorn, uWSGI, etc.)
WSGI_APPLICATION = 'login.wsgi.application'


# =============================================================================
# BASE DE DATOS
# =============================================================================
# Usamos SQLite por simplicidad en desarrollo. En producción habría que cambiar
# a PostgreSQL, MySQL u otra base de datos más robusta para múltiples usuarios.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# =============================================================================
# VALIDACIÓN DE CONTRASEÑAS
# =============================================================================
# Conjunto de validadores que Django aplica al establecer contraseñas.
# Se recomienda mantenerlos en producción para mejorar la seguridad.
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


# =============================================================================
# CONFIGURACIÓN DE DJANGO REST FRAMEWORK (DRF)
# =============================================================================
# Configuración global para todas las vistas de DRF
REST_FRAMEWORK = {
    # Clases de autenticación por defecto: JWT
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # Permisos por defecto: cualquier endpoint requiere autenticación
    # Esto es una medida de seguridad: por defecto todo está protegido,
    # y hay que permitir explícitamente el acceso público donde se necesite.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    # Solo devolvemos JSON, no HTML (típico de API pura)
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
}


# =============================================================================
# CONFIGURACIÓN DE JWT (JSON WEB TOKENS)
# =============================================================================
# Configuración específica de la librería simplejwt
SIMPLE_JWT = {
    # Tiempo de vida del token de acceso (corto, por seguridad)
    # 30 minutos es un buen equilibrio: si roban el token, la ventana es pequeña.
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    
    # Tiempo de vida del refresh token (más largo, para no pedir login cada rato)
    # 7 días permite buena experiencia de usuario sin comprometer demasiado la seguridad.
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    
    # Si es True, al refrescar el token se genera uno nuevo y el viejo se invalida
    'ROTATE_REFRESH_TOKENS': True,
    
    # Si es True, los tokens rotados se añaden a lista negra (requiere app token_blacklist)
    # Esto permite logout efectivo y mayor seguridad.
    'BLACKLIST_AFTER_ROTATION': True,
    
    # Actualiza el campo last_login del usuario al obtener un nuevo token
    # Útil para auditoría y saber la última actividad del usuario.
    'UPDATE_LAST_LOGIN': True,
    
    # Algoritmo de firma y clave secreta
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,      # Usamos la misma SECRET_KEY del proyecto
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    
    # Configuración de headers HTTP
    'AUTH_HEADER_TYPES': ('Bearer',),          # Header: Authorization: Bearer <token>
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    
    # Configuración de claims (campos del token)
    'USER_ID_FIELD': 'id',                     # El campo del modelo User que se usará como ID
    'USER_ID_CLAIM': 'user_id',                 # El nombre del claim en el token
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',                         # Claim para ID único del token
    
    # Configuración de sliding tokens (alternativa, no usada activamente aquí)
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


# =============================================================================
# CONFIGURACIÓN DE CORS (Cross-Origin Resource Sharing)
# =============================================================================
# Permite que el frontend (React en puerto 5173) pueda hacer peticiones al backend.
# Sin esto, el navegador bloquearía las peticiones por política de mismo origen.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",   # Puerto de Vite (desarrollo)
    "http://127.0.0.1:5173",
]

# Permite enviar cookies (como el refresh token HttpOnly) en peticiones cross-origin.
# Necesario para mantener la sesión segura con tokens HttpOnly.
CORS_ALLOW_CREDENTIALS = True


# =============================================================================
# INTERNACIONALIZACIÓN
# =============================================================================
# Configuración de idioma y zona horaria
LANGUAGE_CODE = 'en-us'      # Idioma por defecto
TIME_ZONE = 'UTC'            # Zona horaria (recomendado UTC para APIs)
USE_I18N = True               # Activar internacionalización
USE_TZ = True                 # Usar zona horaria consciente (guardar fechas en UTC)


# =============================================================================
# ARCHIVOS ESTÁTICOS (CSS, JavaScript, imágenes)
# =============================================================================
# URL base para servir archivos estáticos
STATIC_URL = 'static/'