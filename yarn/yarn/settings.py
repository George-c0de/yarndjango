"""
Django settings for yarn project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

# [Unit]
# Description=gunicorn daemon
# After=network.target

# [Service]
# User=django
# Group=django
# WorkingDirectory=/home/django/django_venv/src
# ExecStart=/home/django/django_venv/bin/gunicorn     --access-logfile -     --workers 3     --bind unix:/home/django/django_venv/var/yarn.sock     yarn.wsgi:application

# [Install]
# WantedBy=multi-user.target





# upstream django_server {
#     #server unix:/home/django/django_venv/var/yarn.sock fail_timeout=0;
#     server 127.0.0.1:8000;
# }

# server {
#     listen 80 default_server;
#     listen [::]:80 default_server ipv6only=on;

#     root /usr/share/nginx/html;
#     server_name 134-0-117-229.cloudvps.regruhosting.ru;

#     keepalive_timeout 5;

#     location /static {
#         alias /home/django/django_venv/src/static;
#     }
#     location / {
#         include     proxy_params;
#         proxy_pass  http://django_server;
#     }
# }





    # location / {
    #     include     proxy_params;
    #     proxy_pass  http://unix:/home/django/django_venv/var/yarn.sock;
    # }




# upstream django_server {
#     server unix:/home/django/django_venv/var/yarn.sock fail_timeout=0;
# }

# server {
#     listen 80 default_server;
#     listen [::]:80 default_server ipv6only=on;

#     root /usr/share/nginx/html;
#     server_name http://134-0-117-229.cloudvps.regruhosting.ru/;

#     keepalive_timeout 5;

#     location /static {
#         alias /home/django/django_venv/src/static;
#     }

#     location / {
#         include     proxy_params;
#         proxy_pass  http://django_server;
#     }
# }




# [Unit]
# Description=gunicorn daemon
# After=network.target

# [Service]
# User=django
# Group=django
# WorkingDirectory=/home/django/django_venv/src
# ExecStart=/home/django/django_venv/bin/gunicorn     --access-logfile -     --workers 3     --bind unix:/home/django/django_venv/var/django_project.sock     django_project.wsgi:application

# [Install]
# WantedBy=multi-user.target




from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SITE_URL = 'http://127.0.0.1:8002'
# http://134.0.117.229/
# http://127.0.0.1:8002
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5@)d2p%mwy8iw1%16m1d6c)2vth46j5+2q4)nt944o$2ae6y8t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'nested_inline',
    # "django_extensions",
    'main',
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.  E Y
    'DATETIME_FORMAT': "%d %B %Y %H:%M",
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'yarn.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(os.path.join(BASE_DIR, 'templates')),],
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

WSGI_APPLICATION = 'yarn.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
# STATIC_ROOT = 'static/'
# STATICFILES_DIRS = [
#     BASE_DIR / "static/",
# ]
STATIC_ROOT = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = 'media/'