"""
Django settings for mysite2 project.
Generated by 'django-admin startproject' using Django 4.0.2.
For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
import sys
from datetime import timedelta
import environ
import dj_database_url

env = environ.Env()
# reading .env file
environ.Env.read_env()

# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env("SECRET_KEY")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
#C:\Users\PC\Documents\PYTHON\djangoTravelingBlog

BASE_DIR = Path(__file__).resolve().parent.parent
print(str(BASE_DIR) + "BASE_DIR")
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*4%360imcd6u-p_#x3c^r6o(id=0hd9f^v6y8f!mkv&9*^kt(z'

# Include BOOTSTRAP5_FOLDER in path
BOOTSTRAP5_FOLDER = os.path.abspath(os.path.join(BASE_DIR, "..", "bootstrap5"))

print(BOOTSTRAP5_FOLDER)
if BOOTSTRAP5_FOLDER not in sys.path:
    sys.path.insert(0, BOOTSTRAP5_FOLDER)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['django-traveling-blog.herokuapp.com',
                '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'compressor',
    'sass_processor',
    'storages',
    'sorl.thumbnail'
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_auto_logout.middleware.auto_logout',
]

# logout after 10 minutes of downtime
AUTO_LOGOUT = { 'IDLE_TIME': timedelta(minutes=20),
                'MESSAGE': 'The session has expired. Please login again to continue.',
                'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
                }


MEDIA_ROOT =  os.path.join(BASE_DIR, 'media') 
# media_root - it is absolute path there all collected
MEDIA_URL = 'media/'
# URL that handles the media served from MEDIA_ROOT, used for managing stored files.
ROOT_URLCONF = 'mysite2.urls'
# default URL for login
LOGIN_URL = 'blog:login'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        #os.path.join(BASE_DIR, 'media') 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django_auto_logout.context_processors.auto_logout_client',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite2.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("DATABASE_NAME"),
        'USER': env("DATABASE_USER"),
        # 'PASSWORD': env("DATABASE_PASSWORD"),
        # 'HOST': env("DATABASE_HOST"),
        # 'PORT': env("DATABASE_PORT"),
        # 'CONN_MAX_AGE': 600,         
    }
}


MAX_CONN_AGE=600


if "DATABASE_URL" in os.environ:
    # Configure Django for DATABASE_URL environment variable.
    DATABASES["default"] = dj_database_url.config(
        conn_max_age=MAX_CONN_AGE, ssl_require=False)

    # Enable test database if found in CI environment.
    if "CI" in os.environ:
        DATABASES["default"]["TEST"] = DATABASES["default"]

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
PROJECT_ROOT = os.path.join(os.path.abspath(__file__))

#c:\Users\PC\Documents\PYTHON\djangoTravelingBlog\mysite2\settings.py


STATIC_ROOT = 'static-files/'

#location there where all static files are collected

STATIC_URL = 'static/' 
# this url links to static root there all static files are collected, then we use it in our html with {static /dfs/sdfsf/sdf}

# Extra lookup directories for collectstatic to find static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')     
    ]


#  Add configuration for static files storage using django-storages
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

SASS_PROCESSOR_ROOT = STATIC_ROOT

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
    "sass_processor.finders.CssFinder" 
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
COMPRESS_PRECOMPILERS = ( ('text/x-scss', 'django_libsass.SassCompiler'),)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # Settings for django-bootstrap-v5
# BOOTSTRAP5 = {
#     "error_css_class": "bootstrap5-error",
#     "required_css_class": "bootstrap5-required",
#     "javascript_in_head": True,
# }

DEFAULT_FILE_STORAGE = 'blog.custom_storage.MediaStorage'


AWS_S3_ACCESS_KEY_ID = env("AWS_S3_ACCESS_KEY_ID")
AWS_S3_SECRET_ACCESS_KEY = env("AWS_S3_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")
# AWS_S3_SIGNATURE_VERSION = env("AWS_S3_SIGNATURE_VERSION", default="s3v4")
# AWS_S3_ENDPOINT_URL = env('AWS_S3_ENDPOINT_URL')  
# AWS_QUERYSTRING_AUTH = False

# https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html#canned-acl
# AWS_DEFAULT_ACL = env("AWS_DEFAULT_ACL")

# AWS_PRESIGNED_EXPIRY = env.int("AWS_PRESIGNED_EXPIRY", default=10)  # seconds