from django.conf.urls import url
# from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^$', views.running, name='runs'),
    # url(r'^tables$', views.running_tables, name='run_tables'),
    ]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

