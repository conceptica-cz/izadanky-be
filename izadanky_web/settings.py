"""
Django settings for izadanky_web project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG") == "True"
ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")

if "ALLOWED_HOSTS" in os.environ:
    ALLOWED_HOSTS = [host.strip() for host in os.environ["ALLOWED_HOSTS"].split(",")]
else:
    ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "simple_history",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "corsheaders",
    "django_celery_beat",
    "common",
    "requisitions",
    "references",
    "updates",
    "users",
    "reports",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "izadanky_web.urls"

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

WSGI_APPLICATION = "izadanky_web.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["POSTGRES_DB"],
        "USER": os.environ["POSTGRES_USER"],
        "PASSWORD": os.environ["POSTGRES_PASSWORD"],
        "HOST": os.environ["POSTGRES_HOST"],
        "PORT": os.environ["POSTGRES_PORT"],
    }
}

CONN_MAX_AGE = 180

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "common.authentication.BearerTokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# cors headers

CORS_ALLOW_ALL_ORIGINS = os.environ.get("CORS_ALLOW_ALL_ORIGINS") == "True"

if "CORS_ALLOWED_ORIGINS" in os.environ:
    CORS_ALLOWED_ORIGINS = [
        host.strip() for host in os.environ["CORS_ALLOWED_ORIGINS"].split(",")
    ]
else:
    CORS_ALLOWED_ORIGINS = []


SPECTACULAR_SETTINGS = {
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "TITLE": "iZadanky API",
    "DESCRIPTION": "iZadanky application REST API",
    "VERSION": "1",
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "CET"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

FILE_UPLOAD_MAX_MEMORY_SIZE = 3145728

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

APP_VERSION = (BASE_DIR / Path("version.txt")).read_text()

# PATIENT LOADER

BASE_IPHARM_URL = os.environ.get("BASE_IPHARM_URL", "http://ipharm-app:8000/api/v1")
IPHARM_TOKEN = os.environ.get("IPHARM_TOKEN", "")
PATIENT_LOADER = os.environ.get(
    "PATIENT_LOADER", "requisitions.loaders.ipharm_patient.load_ipharm_patient"
)
IPHARM_TIMEOUT = int(os.environ.get("IPHARM_TIMEOUT", 30))

# REFERENCES AND UPDATES

BASE_ICISELNIKY_URL = os.environ.get(
    "BASE_ICISELNIKY_URL", "http://iciselniky-app:8000/api/v1"
)
ICISELNIKY_TOKEN = os.environ.get("ICISELNIKY_TOKEN", "")


BASE_UNIS_URL = os.environ.get("BASE_UNIS_URL", "http://unis-app:8000/api/v1")
UNIS_TOKEN = os.environ.get("UNIS_TOKEN", "")

DEFAULT_DATA_LOADER = "updates.common.loaders.references_loader"
DEFAULT_MODEL_UPDATER = "updates.common.updaters.simple_model_updater"
DEFAULT_INCREMENTAL_UPDATE_INTERVAL = os.environ.get(
    "DEFAULT_INCREMENTAL_UPDATE_INTERVAL", 15
)
DEFAULT_FULL_UPDATE_INTERVAL = os.environ.get(
    "DEFAULT_INCREMENTAL_UPDATE_INTERVAL", 120
)
DEFAULT_RETRY_DELAY = os.environ.get("DEFAULT_RETRY_DELAY", 3600)


UPDATE_SOURCES = {
    "Clinic": {
        "data_loader_kwargs": {"url": BASE_ICISELNIKY_URL + "/clinics/"},
        "model_updater_kwargs": {
            "model": "references.Clinic",
            "identifiers": ["reference_id"],
        },
        "transformers": ["updates.common.transformers.id_to_reference_id"],
    },
    "Department": {
        "data_loader_kwargs": {"url": BASE_ICISELNIKY_URL + "/departments/"},
        "model_updater_kwargs": {
            "model": "references.Department",
            "identifiers": ["external_id"],
            "relations": {
                "clinic": {
                    "field": "clinic",
                    "key": "reference_id",
                    "delete_source_field": False,
                }
            },
        },
        "transformers": ["updates.common.transformers.delete_id"],
    },
    "Person": {
        "data_loader_kwargs": {"url": BASE_ICISELNIKY_URL + "/persons/"},
        "model_updater_kwargs": {
            "model": "references.Person",
            "identifiers": ["person_number"],
        },
        "transformers": ["updates.common.transformers.delete_id"],
    },
}

# REPORTS

INSURANCE_REPORT_FOLDER = "dosages"
GENERIC_REPORT_FOLDER = "reports"

GENERIC_REPORTS = {}

# CELERY
CELERY_TIMEZONE = TIME_ZONE
REDIS_HOST = os.environ["REDIS_HOST"]
REDIS_PORT = os.environ.get("REDIS_PORT", 6379)
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/1"
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "visibility_timeout": float("inf"),
    "result_chord_ordered": True,
}
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/2"
CELERY_TASK_IGNORE_RESULT = True
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_TRACK_STARTED = True
CELERY_ALWAYS_EAGER = False

CELERY_TASK_DEFAULT_QUEUE = "low_priority"
CELERY_TASK_ROUTES = {
    "requisitions.tasks.load_patient_task": {"queue": "high_priority"}
}

# LOGGING

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(levelname)s %(asctime)s %(name)s %(filename)s %(lineno)s %(funcName)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django.request": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "common": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
        },
        "requisitions": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
        },
        "reports": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
        },
        "updates": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
        },
        "users": {
            "handlers": ["console"],
            "level": LOG_LEVEL,
        },
    },
}

# SENTRY

if os.environ.get("SENTRY_DSN"):
    import sentry_sdk
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.django import DjangoIntegration

    SENTRY_DSN = os.environ["SENTRY_DSN"]
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration(), CeleryIntegration()],
        environment=os.environ.get("SENTRY_ENVIRONMENT", "production"),
        release=APP_VERSION,
    )

# DJANGO DEBUG TOOLBAR
if ENVIRONMENT == "development":
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
    ]
    #    DEBUG_TOOLBAR_CONFIG = {"RESULTS_CACHE_SIZE": 0}

    import socket  # only if you haven't already imported this

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]
