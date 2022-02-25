from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='carga/home_carga.html'), name='carga-home'),
    path('ayudapandemia/', views.carga_datos_entrega_pandemia, name='ayudapandemia-carga'),
    path('empresas/', views.carga_datos_empresa, name='empresas-carga'),
    path('permiso-circulacion/', views.carga_datos_permiso_circulacion, name='permisocirculacion-carga'),
    path('licencias-conducir/', views.carga_datos_licencia_conducir, name='licencias-conducir-carga'),
    path('dom/', views.carga_datos_dom, name='dom-carga'),
    path('exencion-aseo/', views.carga_datos_exencion_aseo, name='aseo-carga'),

    #Descarga excel base
    path('DescargarEjemplo/entregaPandemia/',views.descargar_ejemplo_entrega_pandemia, name='descargar-entrega-pandemia'),
    path('DescargarEjemplo/empresas/',views.descargar_ejemplo_empresa, name='descargar-empresas'),
    path('DescargarEjemplo/licenciaConducir/',views.descargar_ejemplo_licencia_conducir, name='descargar-licencias-conducir'),
    path('DescargarEjemplo/permisoCirculacion/',views.descargar_ejemplo_permiso_circulacion, name='descargar-permiso-circulacion'),
    path('DescargarEjemplo/exencionAseo/',views.descargar_ejemplo_exencion_aseo, name='descargar-exencion-aseo'),
    path('DescargarEjemplo/dom/',views.descargar_ejemplo_dom, name='descargar-dom'),
]    