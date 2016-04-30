from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^balances/', include('balances.urls')),
    url(r'^admin/', admin.site.urls),
]
