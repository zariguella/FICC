from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/', views.login_up, name='login_up'),
    url(r'^logout/', views.logged_out, name='logged_out'),
    url(r'^recovery/', views.recovery, name='recovery'),
    url(r'^registro/', views.registrarse, name='registrarse'),
]
