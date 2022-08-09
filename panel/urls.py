
from django.urls import re_path,path
from panel.api import api
from panel import views
urlpatterns = [
    re_path('^panel/api/',api.urls),
    re_path('^admin/',views.AdminPanel.as_view())
]
