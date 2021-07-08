from django.urls import path
from . import views


urlpatterns = [
    path('', views.calculadorauv, name='calculadorauv'),
    path('cal_uv', views.cal_uv, name='cal_uv'),
]