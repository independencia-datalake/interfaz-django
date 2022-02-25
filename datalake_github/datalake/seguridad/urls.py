from django.urls import path
from django.views.generic import TemplateView
from . import views
from . views import(
  InicioRequerimineto,
)


urlpatterns = [
  path('',TemplateView.as_view(template_name='seguridad/homeseguridad.html'),name="seguridad-home"),
  path('denuncia/',InicioRequerimineto.as_view(), name="denuncia-inicio"),
  path('denuncia/crear/<int:nr>',views.requerimiento_form, name="denuncia-crear"),
  path('denuncia/<int:pk>/',views.requermineto_detalle, name="denuncia-detalle"),
  path('denuncia/<int:pk>/edicion/',views.requermineto_edicion, name="denuncia-edicion"),
  path('denuncia/<int:pk>/delete/',views.requermineto_delete, name="denuncia-delete"),

  path('descargarRequerimiento/',views.descargar_requerimiento_seguridad, name='descargar-requerimiento-seguridad'),

]