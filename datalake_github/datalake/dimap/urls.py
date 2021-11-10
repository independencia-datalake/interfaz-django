from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import(
  InicioEsterilizacion,
  InicioControlPlaga,
)

urlpatterns = [
  path('',TemplateView.as_view(template_name='dimap/homedimap.html'),name="dimap-home"),
  path('esterilizacion/',InicioEsterilizacion.as_view(), name="esterilizacion-inicio"),
  path('esterilizacion/crear/<int:pk>/',views.esterilizacion_form, name="esterilizacion-crear"),
  path('esterilizacion/crear/',views.esterilizacion_verificacion_identidad, name="esterilizacion-verificacion-identidad"),
  path('esterilizacion/<int:pk>/',views.esterilizacion_detail, name="esterilizacion-detail"),
  path('esterilizacion/<int:pk>/delete/',views.esterilizacion_delete, name="esterilizacion-delete"),
  path('controldeplaga/',InicioControlPlaga.as_view(), name="controldeplaga-inicio"),
  path('controldeplaga/crear/',views.controldeplaga_verificacion_identidad, name="controldeplaga-verificacion-identidad"),
  path('controldeplaga/crear/<int:pk>/',views.controldeplaga_form, name="controldeplaga-crear"),
  path('controldeplaga/<int:pk>/',views.controldeplaga_detail, name="controldeplaga-detail"),
  path('controldeplaga/<int:pk>/delete/',views.esterilizacion_delete, name="controldeplaga-delete"),
]