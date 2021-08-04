from django.urls import path
from . import views


urlpatterns = [
    path('', views.calculadorauv, name='calculadorauv'),
    path('cal_uv/', views.cal_uv, name='cal_uv'),
    #AUTOCOMPLETADO
    path('autocompletado-calles',views.autocompete_calles, name='autocompete_calles'),
]