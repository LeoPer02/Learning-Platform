import logging
from datetime import datetime, timedelta
from pathlib import Path
from core.utilities import env
from core.utilities.logging import LoggingConfigurationBuilder


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# General settings

SECRET_KEY = env.as_string("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['*']


# HTTPS configuration. As per Django documentation, these settings should be enabled if we use HTTPS.
# TODO: Check what they actually do?

HTTPS_ENABLED = env.as_bool("HTTPS_ENABLED")
SESSION_COOKIE_SECURE = HTTPS_ENABLED
CRSF_COOKIE_SECURE = HTTPS_ENABLED


# Cors configuration

CORS_ALLOW_ALL_ORIGINS = env.as_bool("CORS_ALLOW_ALL_ORIGINS")
# If CORS_ALLOW_ALL_ORIGINS is True, this setting is ignored
CORS_ALLOWED_ORIGINS = env.as_list("CORS_ALLOWED_ORIGINS")
CSRF_TRUSTED_ORIGINS = env.as_list("CSRF_TRUSTED_ORIGINS")


# Application definition

INSTALLED_APPS = [
    "modeltranslation",  # Must come before all others
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "drf_standardized_errors",
    "corsheaders",
    # Our apps here
    "core",
    "users",
    "course",
    "topic"
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
]

ROOT_URLCONF = "app.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "core" / "templates"],
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
WSGI_APPLICATION = "app.wsgi.application"


# Logging configuration

LOG_FOLDER = BASE_DIR / "logs" / datetime.now().strftime("%Y-%m-%d")

# Use our custom log configuration builder to setup the logger
LOGGING = (
    LoggingConfigurationBuilder()
    # Setup the default formatter
    .add_formatter("default", "[{levelname}] {asctime} {module}: {message}")
    .set_default_formatter("default")
    # Add debug filters
    .add_filter("debug_only", "django.utils.log.RequireDebugTrue")
    .add_filter("prod_only", "django.utils.log.RequireDebugFalse")
    # Add a console handler for debug only
    .add_console_handler("debug_handler", filters=["debug_only"])
    # Setup the root logger
    .add_file_handler("root_handler", LOG_FOLDER / "root.log")
    .modify_root_logger(handlers=["debug_handler", "root_handler"])
    # Setup the default Django logger
    .add_file_handler("django_handler", LOG_FOLDER / "django.log")
    .add_logger("django", ["debug_handler", "django_handler"], level=logging.ERROR, propagate=False)
    # Setup the default Server logger
    .add_file_handler("server_handler", LOG_FOLDER / "server.log")
    .add_logger("django.server", ["debug_handler", "server_handler"], level=logging.ERROR, propagate=False)
    # Add our app-specific loggers
    # Core app
    .add_file_handler("core_handler", LOG_FOLDER / "core.log")
    .add_logger("core", ["debug_handler", "core_handler"], level=logging.ERROR, propagate=False)
).build()


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.as_string("POSTGRES_DB"),
        "USER": env.as_string("POSTGRES_USER"),
        "PASSWORD": env.as_string("POSTGRES_PASSWORD"),
        "HOST": env.as_string("POSTGRES_HOST"),
        "PORT": env.as_string("POSTGRES_PORT"),
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# File handling

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"


# Rest framework settings

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}


# SimpleJWT settings

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=720),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=90),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,  # This hinders performance; can be turned off if necessary.
}


# DRF Standardized Errors settings

DRF_STANDARDIZED_ERRORS = {"EXCEPTION_FORMATTER_CLASS": "core.exceptions.formatter.ExceptionFormatter"}


# DRF Spectacular settings

SPECTACULAR_SETTINGS = {
    "TITLE": env.as_string("SWAGGER_TITLE", "API"),
    "DESCRIPTION": env.as_string("SWAGGER_DESCRIPTION", "API Schema"),
    "VERSION": env.as_string("SWAGGER_API_VERSION", "v1"),
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_PERMISSIONS": (
        "rest_framework.permissions.IsAdminUser"
        if env.as_bool("SWAGGER_ADMIN_ONLY", True)
        else "rest_framework.permissions.AllowAny",
    ),
    "SERVE_AUTHENTICATION": (
        "rest_framework.authentication.SessionAuthentication",  # Same auth for admin page
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}


# User Management

AUTH_USER_MODEL = "users.User"
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
AUTHENTICATION_BACKENDS = ["users.authentication.AuthenticationBackend"]
AUTH_USER_REGISTRATION_ENABLED = env.as_bool("AUTH_USER_REGISTRATION_ENABLED", True)


# Miscellaneous Settings
LANGUAGE_CODE = "en"
LANGUAGES = [
    ("en", "English"),
    ("de", "German"),
    ("el", "Greek"),
    ("pt", "Portuguese"),
    ("hr", "Croatian"),
    ("fr", "French"),
]
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
COMMAND_WAIT_FOR_DB_MAX_RETRIES = 10
