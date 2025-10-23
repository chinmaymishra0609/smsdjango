from pathlib import Path
from decouple import config, UndefinedValueError
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-3qlook39nycb2(i8%qq-hq#w=0%7ur1ixccfisini)r^t@^in*"

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = config("DEBUG", "False") == "True"

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    "django_celery_beat",
    "django_celery_results",
    "django_channels",
    "django_celery",
    "core",
    "student",
    "user",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "smsdjango.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "smsdjango.wsgi.application"
ASGI_APPLICATION = "smsdjango.asgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

try:
    DB_ENGINE = config("DB_ENGINE")
except UndefinedValueError:
    DB_ENGINE = "django.db.backends.sqlite3"

if DB_ENGINE == "django.db.backends.sqlite3":
    DATABASES = {
        "default": {
            "ENGINE": config("DB_ENGINE"),
            "NAME": BASE_DIR / config("DB_NAME", default="db.sqlite3"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": DB_ENGINE,
            "NAME": config("DB_NAME"),
            "USER": config("DB_USER"),
            "PASSWORD": config("DB_PASSWORD"),
            "HOST": config("DB_HOST", "localhost"),
            "PORT": config("DB_PORT", "5432"),
        }
    }

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# Email settings
EMAIL_BACKEND       = config("EMAIL_BACKEND")
EMAIL_HOST          = config("EMAIL_HOST")
EMAIL_PORT          = config("EMAIL_PORT")
EMAIL_USE_TLS       = config("EMAIL_USE_TLS")
EMAIL_HOST_USER     = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL  = config("DEFAULT_FROM_EMAIL")

# Redis settings
CELERY_BROKER_URL = "redis://localhost:6379/0"
# CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "django-db"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Kolkata"
CELERY_RESULT_EXTENDED = True
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_BEAT_SCHEDULE = {
    "clear-session-cache-in-every-10-seconds": {
        "task": "ClearSessionCacheTask",
        "schedule": timedelta(seconds=10),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
# Add this in production
STATIC_ROOT = BASE_DIR / "static"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"