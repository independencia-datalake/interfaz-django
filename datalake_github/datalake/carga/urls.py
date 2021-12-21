from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='carga/home_carga.html'), name='carga-home'),
    path('ayudapandemia/', views.carga_datos_entrega_pandemia, name='ayudapandemia-carga'),
    path('empresas/', views.carga_datos_empresa, name='empresas-carga'),
    path('permiso_circulacion/', views.carga_datos_permiso_circulacion, name='permisocirculacion-carga'),
    path('patentes_vehiculares/', views.carga_datos_patentes_vehiculares, name='patentesvehiculares-carga'),
]    