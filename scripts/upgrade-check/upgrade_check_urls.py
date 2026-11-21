"""Project URLs plus media serving, which runserver skips when DEBUG is off."""

from django.conf import settings
from django.urls import re_path
from django.views.static import serve
from pythonie.urls import urlpatterns as project_urlpatterns

urlpatterns = [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    *project_urlpatterns,
]
