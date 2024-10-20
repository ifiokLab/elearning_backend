"""
Django settings for elearning_backend project.

Generated by 'django-admin startproject' using Django 4.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
import os
import dj_database_url
from azure.storage.blob import BlobServiceClient
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-0q8s+5x&(acv*3=0%5ocb__jc^bz=w9#y+ig1m@z&wrn8(k8ym'
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['elearning-backend.azurewebsites.net','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'App',
    'rest_framework',
    'rest_framework.authtoken',
    "corsheaders",
    'rest_auth',
    'cities_light',
    'rest_auth.registration',
]

#CORS_ALLOW_ALL_ORIGINS = True
#CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',  # React development server
    'https://thankful-water-077d75a0f.4.azurestaticapps.net',  # Your Azure static web app domain
    # Add other allowed origins as needed
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

ACCOUNT_EMAIL_VERIFICATION = 'none' 

AUTHENTICATION_CLASSES = (
    'allauth.account.auth_backends.AuthenticationBackend',
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.TokenAuthentication',
)
"""AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]"""
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        # ...
    ],
    # ...
}

ROOT_URLCONF = 'elearning_backend.urls'

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

WSGI_APPLICATION = 'elearning_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL')),
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
#STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATIC_ROOT = BASE_DIR / 'staticfiles'


DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'

"""AZURE_BLOB_SERVICE_OPTIONS = {
    'connection_timeout': 780,  # Set to None to disable the connection timeout
    'socket_timeout': 780,  # Set to None to disable the socket timeout
}"""
AZURE_CONNECTION_STRING = os.environ.get('AZURE_CONNECTION_STRING')
AZURE_ACCOUNT_NAME = "elearningappstorage"
AZURE_CONTAINER = 'media'  # Replace with your container name
#AZURE_CUSTOM_DOMAIN = "https://elearningappstorage.blob.core.windows.net/media/"
AZURE_LOCATION = 'East US' 

azure_service_client = BlobServiceClient.from_connection_string(os.environ.get('AZURE_CONNECTION_STRING'))

#azure_service_client.socket_timeout = 1800
azure_container_client = azure_service_client.get_container_client(os.environ.get('AZURE_CONTAINER'))

print('azure_service_client.timeout:',azure_service_client)

# Optional: Set a custom domain for serving media files

MEDIA_URL = "https://elearningappstorage.blob.core.windows.net/media/"
MEDIA_ROOT = None  # Media files are stored in Azure Blob Storage
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'App.myuser'

#MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
print('STRIPE_SECRET_KEY:',STRIPE_SECRET_KEY) 