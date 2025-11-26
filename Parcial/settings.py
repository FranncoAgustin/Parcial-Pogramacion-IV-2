from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# CONFIGURACIÓN BÁSICA
# =========================

# Para simplificar el parcial dejamos una key fija,
# pero en Render podés sobreescribirla con SECRET_KEY en env vars.
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-2ke0f#rl5rx)9wn0lq0aeqebe$n!vlekb=p4^7dpo-^^gperf#"
)

# DEBUG: True en local, False en Render (lo seteás en env)
DEBUG = os.environ.get("DEBUG", "True") == "True"

# ALLOWED_HOSTS: para local y Render
ALLOWED_HOSTS = ["*", "localhost", "127.0.0.1"]

# Para evitar problemas de CSRF en Render (lo completás después con tu dominio)
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
    # Whitenoise para servir estáticos en Render
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

# Por defecto, SQLite (local / desarrollo)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Si en Render seteás DATABASE_URL, se usa Postgres automáticamente
if os.environ.get("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.config(
        default=os.environ["DATABASE_URL"],
        conn_max_age=600,
        ssl_require=False,  # en Render suele ser True, pero para el parcial podés dejarlo así
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

# Donde collectstatic los deja (Render)
STATIC_ROOT = BASE_DIR / "staticfiles"

# Para archivos estáticos propios (si querés)
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Whitenoise: comprime y cachea
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# =========================
# LOGIN / LOGOUT
# =========================

LOGIN_URL = "cuentas:login"
LOGIN_REDIRECT_URL = "alumnos:dashboard"
LOGOUT_REDIRECT_URL = "cuentas:login"


# =========================
# EMAIL
# =========================

if DEBUG:
    # En local: ver mails en consola
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "no-reply@parcial.local"
else:
    # En Render: SMTP real (si lo configurás)
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
    EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)


# =========================
# PRIMARY KEY
# =========================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
