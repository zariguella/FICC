from django.conf.urls import include, url
from django.contrib import admin
from principal import views
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^inicio/', views.index, name='index'),
    url(r'^ver_logs/', views.ver_logs, name='ver_logs'),
    url(r'^balances/', include('balances.urls')),
    url(r'^egresos/', include('egresos.urls')),
    url(r'^ingresos/', include('ingresos.urls')),
    url(r'^libros_contables/', include('libros_contables.urls')),
    url(r'^usuarios/', include('usuarios.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT}),
]
