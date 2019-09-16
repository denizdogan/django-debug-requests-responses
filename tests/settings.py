DEBUG = True

SECRET_KEY = "ddrr"

INSTALLED_APPS = ("ddrr",)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    }
]

ROOT_URLCONF = "tests.urls"

MIDDLEWARE = ("ddrr.middleware.DebugRequestsResponses",)
