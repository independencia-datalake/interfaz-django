from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import(
  InicioEsterilizacion,
  InicioControlPlaga,
  InicioSeguridadDIMAP,
  EdicionControlPlaga,
  EdicionSeguridadDIMAP,
)

urlpatterns = [
  path('',TemplateView.as_view(template_name='dimap/homedimap.html'),name="dimap-home"),
  path('esterilizacion/',InicioEsterilizacion.as_view(), name="esterilizacion-inicio"),
  path('esterilizacion/crear/<int:pk>/',views.esterilizacion_form, name="esterilizacion-crear"),
  path('esterilizacion/crear/',views.esterilizacion_verificacion_identidad, name="esterilizacion-verificacion-identidad"),
  path('esterilizacion/<int:pk>/',views.esterilizacion_detail, name="esterilizacion-detail"),
  path('esterilizacion/<int:pk>/edicion/',views.esterilizacion_edicion, name="esterilizacion-edicion"),
  path('esterilizacion/<int:pk>/delete/',views.esterilizacion_delete, name="esterilizacion-delete"),
  path('controldeplaga/',InicioControlPlaga.as_view(), name="controldeplaga-inicio"),
  path('controldeplaga/crear/',views.controldeplaga_verificacion_identidad, name="controldeplaga-verificacion-identidad"),
  path('controldeplaga/crear/<int:pk>/',views.controldeplaga_form, name="controldeplaga-crear"),
  path('controldeplaga/<int:pk>/',views.controldeplaga_detail, name="controldeplaga-detail"),
  path('controldeplaga/<int:pk>/edicion/',EdicionControlPlaga.as_view(), name="controldeplaga-edicion"),
  path('controldeplaga/<int:pk>/delete/',views.esterilizacion_delete, name="controldeplaga-delete"),
  path('seguridad/',InicioSeguridadDIMAP.as_view(), name="seguridad-inicio"),
  path('seguridad/crear/',views.seguridad_verificacion_identidad, name="seguridad-verificacion-identidad"),
  path('seguridad/crear/<int:pk>/',views.seguridad_form, name="seguridad-crear"),
  path('seguridad/<int:pk>/',views.seguridad_detail, name="seguridad-detail"),
  path('seguridad/<int:pk>/edicion/',EdicionSeguridadDIMAP.as_view(), name="seguridad-edicion"),
  path('seguridad/<int:pk>/delete/',views.seguridad_delete, name="seguridad-delete"),
]