from django.urls import path
from . import views
from .views import *

urlpatterns = [
    #COMPROBANTE DE VENTA
    path('ComprobanteDeVenta/',views.comprobante_venta, name='comprobanteventa-create'),
    #PRODUCTO FARMACIA
    path('ProductoFarmacia/', InicioProductoFarmacia.as_view(), name='productofarmacia-inicio'),
    path('ProductoFarmacia/crear/', CrearProductoFarmacia.as_view(), name='productofarmacia-create'),
    path('ProductoFarmacia/<int:pk>/',DetalleProductoFarmacia.as_view(),name="productofarmacia-detail"),
    path('ProductoFarmacia/<int:pk>/edicion/',EdicionProductoFarmacia.as_view(),name="productofarmacia-update"),
]