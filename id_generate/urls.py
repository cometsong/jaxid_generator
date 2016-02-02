from django.conf.urls import url
# from django.conf.urls.static import static

from . import views
from . import generate

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^batch$', generate.batch, name='batch'),
    ]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

