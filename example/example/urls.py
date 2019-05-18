from django.urls import path

from app.views import index
from app.views import ugly_xml
from app.views import unauthorized

urlpatterns = [path("", index), path("401", unauthorized), path("ugly_xml", ugly_xml)]
