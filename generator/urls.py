from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^manage/id_generate', include('id_generate.urls')),
    url(r'^manage/', include(admin.site.urls)),
    # url(r'^files/', include('filer.urls')),
    # url(r'^', include('id_generate.urls')),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
