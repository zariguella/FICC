from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^egresos_list/', views.list_egresos, name='list_egresos'),
    url(r'^carga_egresos/', views.carga, name='carga'),
    url(r'^egresos_edit/(?P<e_id>\d+)', views.edit_egresos, name='edit_egresos'),
    url(r'^egresos_edit/', views.list_egresos, name='list_egresos'),
    url(r'^egresos_update/', views.update_egresos, name='update_egresos'),
    url(r'^solicitar_planilla_egresos/', views.solicitar_planilla_egresos, name='solicitar_planilla_egresos'),
    url(r'^generar_planilla_csv_egresos/', views.generar_planilla_csv_egresos, name='generar_planilla_csv_egresos'),
]
