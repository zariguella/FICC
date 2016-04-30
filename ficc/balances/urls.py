from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^balances/$', views.index, name='index'),
    url(r'^balances/csv/$', views.index, name='index'),
    url(r'^generar_balance', views.generar_balance, name='generar_balance'),
]
