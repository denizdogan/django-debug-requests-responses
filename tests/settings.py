DEBUG = True

USE_TZ = False

SECRET_KEY = "ddrr"

INSTALLED_APPS = ("ddrr",)

ROOT_URLCONF = "tests.urls"

MIDDLEWARE = ("ddrr.middleware.DebugRequestsResponses",)
