from django.urls import path
from . import views

urlpatterns = [
  path('',views.paginaprincipal,name="core-home"),
  path('quienes/',views.quienes,name="core-quienes"),
  path('qya/',views.qya,name="core-qya"),
]