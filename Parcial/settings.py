from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Cargar variables del .env local
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# CONFIGURACIÓN BÁSICA
# =========================

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-2ke0f#rl5rx)9wn0lq0aeqebe$n!vlekb=p4^7dpo-^^gperf#"
)

DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = ["*", "localhost", "127.0.0.1"]

CSRF_TRUSTED_ORIGINS = os.environ.get(
    "CSRF_TRUSTED_ORIGINS",
    "http://localhost,http://127.0.0.1"
).split(",")


# =========================
# APLICACIONES
# =========================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "alumnos",
    "cuentas",
    "scraper",
]


# =========================
# MIDDLEWARE
# =========================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "Parcial.urls"


# =========================
# TEMPLATES
# =========================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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


WSGI_APPLICATION = "Parcial.wsgi.application"


# =========================
# BASE DE DATOS
# =========================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

if os.environ.get("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.config(
        default=os.environ["DATABASE_URL"],
        conn_max_age=600,
        ssl_require=False,
    )


# =========================
# PASSWORD VALIDATION
# =========================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# =========================
# INTERNACIONALIZACIÓN
# =========================

LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"

USE_I18N = True
USE_TZ = True


# =========================
# ARCHIVOS ESTÁTICOS
# =========================

STATIC_URL = "static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# =========================
# LOGIN / LOGOUT
# =========================

LOGIN_URL = "cuentas:login"
LOGIN_REDIRECT_URL = "alumnos:dashboard"
LOGOUT_REDIRECT_URL = "cuentas:login"


# =========================
# EMAIL (SendGrid)
# =========================

DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "brguix57@gmail.com")

# → ESTA debe existir tanto en tu .env local como en Render
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")


# =========================
# PRIMARY KEY
# =========================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
