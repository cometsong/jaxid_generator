from django.conf import settings
from django.conf.urls import include, url

import django_databrowse
from id_generate.admin import idadmin

urlpatterns = [
    url(r'^manage/', include(idadmin.urls), name='admin'),
    url(r'^$', idadmin.login, name='login'),
    url(r'^databrowse/(.*)', django_databrowse.site.root),

    # url(r'^', include('id_generate.urls')),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
