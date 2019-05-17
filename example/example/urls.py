from django.urls import path

from app.views import index
from app.views import unauthorized

urlpatterns = [path("", index), path("401", unauthorized)]
