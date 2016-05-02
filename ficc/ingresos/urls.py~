from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ingresos_list/', views.list_ingresos, name='list_ingresos'),
    url(r'^carga_ingresos/', views.carga, name='carga'),
    url(r'^ingresos_edit/(?P<e_id>\d+)', views.edit_ingresos, name='edit_ingresos'),
    url(r'^ingresos_edit/', views.list_ingresos, name='list_ingresos'),
    url(r'^ingresos_update/', views.update_ingresos, name='update_ingresos'),
    url(r'^solicitar_planilla_ingresos/', views.solicitar_planilla_ingresos, name='solicitar_planilla_ingresos'),
    url(r'^generar_planilla_csv_ingresos/', views.generar_planilla_csv_ingresos, name='generar_planilla_csv_ingresos'),
]
