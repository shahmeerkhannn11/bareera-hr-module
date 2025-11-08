from pathlib import Path
import os

# -------------------------------------------------------------
# BASE SETTINGS
# -------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-CHANGE_THIS_TO_YOUR_SECRET_KEY'

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'shahmeerkhan1.pythonanywhere.com']

# -------------------------------------------------------------
# INSTALLED APPS
# -------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hr',  # your HR app
]

# -------------------------------------------------------------
# MIDDLEWARE
# -------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -------------------------------------------------------------
# URL CONFIGURATION
# -------------------------------------------------------------
ROOT_URLCONF = 'bareera_hr.urls'

# -------------------------------------------------------------
# TEMPLATE SETTINGS
# -------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # 👇 Django will first look in this directory for all templates (including admin overrides)
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],

        # Enable Django to find templates within installed apps as well
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

WSGI_APPLICATION = 'bareera_hr.wsgi.application'

# -------------------------------------------------------------
# DATABASE CONFIGURATION
# -------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -------------------------------------------------------------
# PASSWORD VALIDATION
# -------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------------------------------------
# INTERNATIONALIZATION
# -------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Karachi'
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------
# STATIC & MEDIA FILES
# -------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# -------------------------------------------------------------
# DEFAULT PRIMARY KEY FIELD TYPE
# -------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
