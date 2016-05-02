from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^asientos_list/', views.list_asientos, name='list_asientos'),
    url(r'^asientos_edit/(?P<a_id>\d+)', views.edit_asientos, name='edit_asientos'),
    url(r'^asientos_update/', views.update_asientos, name='update_asientos'),
    url(r'^cargar_asiento/', views.cargar_asiento, name='cargar_asiento'),
]
