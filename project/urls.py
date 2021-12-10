from django.conf.urls import re_path
from django.contrib import admin

urlpatterns = [
    re_path(r'^', admin.site.urls),
]
