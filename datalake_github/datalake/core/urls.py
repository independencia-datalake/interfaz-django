from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
  path('',TemplateView.as_view(template_name='core/home.html'),name="core-home"),
  path('quienes/',TemplateView.as_view(template_name='core/quienes.html'),name="core-quienes"),
  path('qya/',TemplateView.as_view(template_name='core/qya.html'),name="core-qya"),
]