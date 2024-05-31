import os

from django.conf import settings
from django.urls import path, re_path
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls

# from wagtail.search import urls as wagtailsearch_urls
from wagtail.documents import urls as wagtaildocs_urls

urlpatterns = [
    re_path(r"^django-admin/", admin.site.urls),
    re_path(r"^admin/", include(wagtailadmin_urls)),
    #    url(r'^search/', include(wagtailsearch_urls)),
    re_path(r"^documents/", include(wagtaildocs_urls)),
    path(r"", include(wagtail_urls)),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL + "images/",
        document_root=os.path.join(settings.MEDIA_ROOT, "images"),
    )
