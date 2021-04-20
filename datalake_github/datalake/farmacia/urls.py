from django.urls import path
from . import views
from .views import *

urlpatterns = [
    #COMPROBANTE DE VENTA
    path('<str:pk>/',views.comprobante_venta, name='comprobante_venta'),
]