from django.urls import path
from . import views
from .views import ListaFormularioOMIL

urlpatterns = [
  path('',ListaFormularioOMIL.as_view(),name="core-home"),
  path('quienes/',views.quienes,name="core-quienes"),
  path('qya/',views.qya,name="core-qya"),
]