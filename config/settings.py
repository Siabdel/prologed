"""
Django settings for prologed project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent.parent
# Directory project au meme niveau de settings.py
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-wls+z0u*ci0ots^zskvuzhf4e!d+0k4o--7=)3dx)pu$jq_*_b"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Application definition

INSTALLED_APPS = [
    # django contrib 
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    ##
    # 3rd-party apps
    'rest_framework', # new
    'rest_framework.authtoken',
    "dj_rest_auth",
    # debug tools
    'debug_toolbar', # new
    'corsheaders', 
    # User Authentication
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #
      # Third party
    'crispy_forms',
    #'crispy_bootstrap5',  # Si vous utilisez Bootstrap 5
    "crispy_bootstrap4",
    "django_extensions",
    # local
    'logyapp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",  # new
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
    # debug 
    'debug_toolbar.middleware.DebugToolbarMiddleware', # new
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'Fr-fr'

DEFAULT_CHARSET='UTF-8'

TIME_ZONE = 'UTC'
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
# Lorsque USE_TZ vaut True et que la base de données ne gère pas les fuseaux horaires (par ex. SQLite, MySQL, Oracle), Django lit et écrit les dates/heures en heure locale en fonction de cette option quand elle est définie et en UTC si elle ne l’est pas.

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static" )
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'staticfiles'),
    os.path.join(BASE_DIR, 'media'),
    os.path.join(BASE_DIR, 'media', 'upload'),
]
