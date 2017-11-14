from django.conf import settings
from django.conf.urls import include, url

from id_generate.admin import admin_gen

urlpatterns = [
    url(r'^manage/id_generate', include('id_generate.urls')),
    url(r'^manage/', include(admin_gen.urls)),

    # url(r'^files/', include('filer.urls')),
    # url(r'^', include('id_generate.urls')),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
