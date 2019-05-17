import ddrr

DEBUG = True

SECRET_KEY = "ddrr"

INSTALLED_APPS = ("ddrr",)

TEMPLATES = [
    {"BACKEND": "django.template.backends.django.DjangoTemplates", "APP_DIRS": True}
]

LOGGING = {"version": 1}

ROOT_URLCONF = "tests.urls"

ddrr.quick_setup()
