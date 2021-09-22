from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
  path('',TemplateView.as_view(template_name='core/home.html'),name="core-home"),
  path('persona/',views.persona ,name="persona"),
  path('persona/crear',views.persona_crear,name="persona-crear"),
  path('quienes/',TemplateView.as_view(template_name='core/quienes.html'),name="core-quienes"),
  path('qya/',TemplateView.as_view(template_name='core/qya.html'),name="core-qya"),
]