from django.urls import re_path

from mobile.api import api

urlpatterns = [
re_path('^mobile/api/',api.urls),
]