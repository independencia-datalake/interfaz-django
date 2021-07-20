from django.urls import path
from . import views
from .views import (
    #COMPROBANTE DE VENTA
    InicioComprobanteVenta,
    EdicionComprobanteVenta,
    
    #PRODUCTO VENDIDO
    EdicionProductoVendido,
    
    #PRODUCTO FARMACIA
    InicioProductoFarmacia,
    DetalleProductoFarmacia,
    CrearProductoFarmacia,
    EdicionProductoFarmacia,
)

urlpatterns = [
    #COMPROBANTE DE VENTA
    path('ComprobanteDeVenta/',InicioComprobanteVenta.as_view(), name="comprobanteventa-inicio"),
    path('ComprobanteDeVenta/crear/',views.comprobante_venta_form, name='comprobanteventa-create'),
    path('ComprobanteDeVenta/<int:pk>/',views.comprobante_venta_detail, name='comprobanteventa-detail'),
    path('ComprobanteDeVenta/<int:pk>/edicion/',EdicionComprobanteVenta.as_view(), name='comprobanteventa-update'),
    path('ComprobanteDeVenta/<int:pk>/delete/',views.comprobante_venta_delete, name='comprobanteventa-delete'),
    path('DescargarComprobantes',views.descargar_comprobantes, name='descargar-comprobantes'),
    #PRODUCTO VENDIDO
    path('ProductoVendido/<int:pk>/edicion/',EdicionProductoVendido.as_view(),name="productovendido-update"),
    #PRODUCTO FARMACIA
    path('ProductoFarmacia/', InicioProductoFarmacia.as_view(), name='productofarmacia-inicio'),
    path('ProductoFarmacia/crear/', CrearProductoFarmacia.as_view(), name='productofarmacia-create'),
    path('ProductoFarmacia/<int:pk>/',DetalleProductoFarmacia.as_view(),name="productofarmacia-detail"),
    path('ProductoFarmacia/<int:pk>/edicion/',EdicionProductoFarmacia.as_view(),name="productofarmacia-update"),
    path('ProductoFarmacia/<int:pk>/delete/',views.producto_farmacia_delete, name='productofarmacia-delete'),
]