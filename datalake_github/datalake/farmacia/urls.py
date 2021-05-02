from django.urls import path
from . import views
from .views import *

urlpatterns = [
    #COMPROBANTE DE VENTA
    path('ComprobanteDeVenta/',views.comprobante_venta, name='comprobanteventa-create'),
]