"""
Django settings for composeexample project.
Generated by 'django-admin startproject' using Django 3.2.12.
For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

import mimetypes
mimetypes.add_type("text/css", ".css", True)
mimetypes.add_type("text/javascript", ".js", True)
  
# Build paths inside the project like this: BASE_ / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ay1^sva0%7-oag2+k6_pnv#!#957q_*x2n%e--9@*&mry4070t'

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
    'django.contrib.gis',
    'leaflet',
    'djgeojson',
    'web.apps.WebConfig',
    'social_django',
    'upload.apps.UploadConfig',
    'account',
    'django_apscheduler',
]
SCHEDULER_CONFIG = {
    "apscheduler.jobstores.default": {
        "class": "django_apscheduler.jobstores:DjangoJobStore"
    },
    'apscheduler.executors.processpool': {
        "type": "threadpool"
    },
}
SCHEDULER_AUTOSTART = True
AUTH_USER_MODEL = 'account.Account'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware', 

]
AUTHENTICATION_BACKENDS = (
   # 'social_core.backends.open_id.OpenIdAuth',  # OpenId用
   # 'social_core.backends.google.GoogleOpenId',  # Google OpenId用
    'social_core.backends.google.GoogleOAuth2',  # Google OAuth2用

   # 'social_core.backends.github.GithubOAuth2',  # Github用
   # 'social_core.backends.twitter.TwitterOAuth',  # Twitter用
   # 'social_core.backends.facebook.FacebookOAuth2',  # Facebook用

    'django.contrib.auth.backends.ModelBackend',  # デフォルトバックエンド、必須。
)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '453255475639-uu7bvpomb3re8bsrr0drvhpvmss3fncb.apps.googleusercontent.com'  # クライアントID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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' # クライアント シークレット

LOGIN_URL = 'account:login'
LOGIN_REDIRECT_URL = 'account:home'
LOGOUT_REDIRECT_URL = 'account:top'
SOCIAL_AUTH_POSTGRES_JSONFIELD = True

ROOT_URLCONF = 'composeexample.urls'

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
                
                'social_django.context_processors.backends', 
                'social_django.context_processors.login_redirect', 
            ],
        },
    },
]

WSGI_APPLICATION = 'composeexample.wsgi.application'


# Data
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ja'     # 値を変更
TIME_ZONE = 'Asia/Tokyo' # 値を変更

USE_I18N = True

USE_L10N = True

USE_TZ = True

#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#MEDIA_URL = '/media/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
FILE_UPLOAD_PERMISSIONS = 0o644
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [BASE_DIR / 'static_local',]
PROJECT_DIR= os.path.dirname(os.path.abspath(__file__))
GDAL_LIBRARY_PATH = "/usr/lib/libgdal.so.28"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
