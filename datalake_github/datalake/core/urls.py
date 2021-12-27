from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
  #path('',TemplateView.as_view(template_name='core/home.html'),name="core-home"),
  path('', views.inicio, name="core-home"),
  path('persona/',views.persona ,name="persona"),
  # path('persona/crear/<int:pk>/',views.persona_crear,name="persona-crear"),
  path('persona/crear/<int:pk>/<str:n_iden>/<ty_iden>/',views.persona_crear,name="persona-crear"),
  path('quienes/',TemplateView.as_view(template_name='core/quienes.html'),name="core-quienes"),
  path('qya/',TemplateView.as_view(template_name='core/qya.html'),name="core-qya"),
]