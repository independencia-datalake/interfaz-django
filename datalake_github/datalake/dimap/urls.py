from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import(
  InicioEsterilizacion,
)

urlpatterns = [
  path('',TemplateView.as_view(template_name='dimap/homedimap.html'),name="dimap-home"),
  path('esterilizacion/',InicioEsterilizacion.as_view(), name="esterilizacion-inicio"),
  path('esterilizacion/crear',views.esterilizacion_form, name="esterilizacion-crear"),
  path('esterilizacion/<int:pk>/',views.esterilizacion_detail, name="esterilizacion-detail"),
  path('esterilizacion/<int:pk>/delete/',views.esterilizacion_delete, name="esterilizacion-delete"),
]