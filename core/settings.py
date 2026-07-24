from pathlib import Path

import environ
from django.contrib.messages import constants as message_constants

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
env = environ.Env(
    DEBUG=(bool, False),  # secure default: off unless .env says otherwise
    TIME_ZONE=(str, "UTC"),
    ALLOWED_HOSTS=(list, []),
)
environ.Env.read_env(BASE_DIR / ".env")

# SECURITY WARNING: keep the secret key used in production secret!
# No default on purpose — the app must refuse to start without an explicit key.
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_select2",
    "website",
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

ROOT_URLCONF = "core.urls"

WSGI_APPLICATION = "core.wsgi.application"

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
        "CONN_MAX_AGE": 60,  # reuse connections for up to 60s (persistent connections)
    }
}

# ---------------------------------------------------------------------------
# Cache (Redis) — also backs django_select2 widget state
# ---------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL"),  # required — see .env.example
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

SELECT2_CACHE_BACKEND = "default"

# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------
AUTH_USER_MODEL = "website.User"

LOGIN_URL = "website:home"  # used by @login_required

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------------
# Internationalization
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "uk"
TIME_ZONE = env("TIME_ZONE")
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Static & media files
# ---------------------------------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Messages -> Bootstrap alert classes
# ---------------------------------------------------------------------------
MESSAGE_TAGS = {
    message_constants.DEBUG: "secondary",
    message_constants.INFO: "info",
    message_constants.SUCCESS: "success",
    message_constants.WARNING: "warning",
    message_constants.ERROR: "danger",  # error -> Bootstrap 'danger'
}

# ---------------------------------------------------------------------------
# Logging — stream every SQL query to the console (dev aid)
# ---------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "WARNING",
        },
    },
}

# ---------------------------------------------------------------------------
# Development-only tooling (debug toolbar) — never active in production
# ---------------------------------------------------------------------------
if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.insert(
        MIDDLEWARE.index("django.middleware.common.CommonMiddleware"),
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )
    INTERNAL_IPS = ["127.0.0.1"]

# ---------------------------------------------------------------------------
# Production hardening — only when DEBUG is off
# Each line maps to a `manage.py check --deploy` warning.
# ---------------------------------------------------------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_PROXY_SSL_HEADER = (
        "HTTP_X_FORWARDED_PROTO",
        "https",
    )  # trust proxy's https header
