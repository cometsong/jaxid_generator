from django.conf.urls import include, url
from django.contrib import admin
from id_generate import generate

urlpatterns = [
    url(r'^admin/generate_new_jaxids$',
        generate.generate_new_ids),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^files/', include('filer.urls')),
    # url(r'^', include('id_generate.urls')),
]
