"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

mandatory_settings = ["DATABASE_URL"]
optional_settings = ["GS_BUCKET_NAME"]

# If our mandatory settings aren't all already defined as environment variables
# try pulling them from Secret Manager
if not all (k in os.environ.keys() for k in set(mandatory_settings)):
    from . import sm_helper
    try:
        secrets = sm_helper.access_secrets(mandatory_settings + optional_settings)
        os.environ.update(secrets)
    except:
        print("mandatory_settings not found in SM")

env = environ.Env(DEBUG=(bool, False))
#env.read_env(os.environ.get("ENV_PATH", ".env"))

DEBUG = env('DEBUG')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kg_mk_=!u+%-=^wzob*kz3(f@(7ou0hfu!w&2u%r4u3mpdy4rv'

if "CURRENT_HOST" in os.environ:
    HOSTS = []
    for h in env.list("CURRENT_HOST"):
        if "://" in h:
            h = h.split("://")[1]
        HOSTS.append(h)
else:
    # Assume localhost if no CURRENT_HOST
    HOSTS = ["localhost"]

ALLOWED_HOSTS = ["127.0.0.1"] + HOSTS


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api.apps.ApiConfig',
    'rest_framework_swagger'
]

REST_FRAMEWORK = { 
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema' 
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

STATIC_ROOT = "/static/"

if "GS_BUCKET_NAME" in os.environ:
    GS_BUCKET_NAME = env("GS_BUCKET_NAME", None)
    if GS_BUCKET_NAME:
        DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
        STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
        GS_DEFAULT_ACL = "publicRead"
        INSTALLED_APPS += ["storages"]
    else:
        print("GS_BUCKET_NAME not found")
else:
    print("GS_BUCKET_NAME not found")

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {"default": env.db()}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
