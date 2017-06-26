from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^manage/', include(admin.site.urls)),
    # url(r'^files/', include('filer.urls')),
    # url(r'^', include('id_generate.urls')),
]
