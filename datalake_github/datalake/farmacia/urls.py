from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import (
    #COMPROBANTE DE VENTA
    InicioComprobanteVenta,
    EdicionComprobanteVenta,
    
    #PRODUCTO VENDIDO
    EdicionProductoVendido,
    
    #PRODUCTO FARMACIA
    InicioProductoFarmacia,
    EdicionProductoFarmacia,
)

urlpatterns = [
    path('',TemplateView.as_view(template_name='farmacia/homefarmacia.html'),name="farmacia-home"),
    #COMPROBANTE DE VENTA
    path('ComprobanteDeVenta/',InicioComprobanteVenta.as_view(), name="comprobanteventa-inicio"),
    path('ComprobanteDeVenta/<int:pk>/crear/',views.comprobante_venta_form, name='comprobanteventa-create'),
    path('ComprobanteDeVenta/<int:pk>/',views.comprobante_venta_detail, name='comprobanteventa-detail'),
    path('ComprobanteDeVenta/<int:pk>/edicion-identificacion/',EdicionComprobanteVenta.as_view(), name='comprobanteventa-update'),
    path('ComprobanteDeVenta/<int:pk>/edicion/',views.comprobante_venta_edicion, name='comprobanteventa-edicion'),
    path('ComprobanteDeVenta/<int:pk>/delete/',views.comprobante_venta_delete, name='comprobanteventa-delete'),
    path('DescargarComprobantes',views.descargar_comprobantes, name='descargar-comprobantes'),
    #PRODUCTO VENDIDO
    path('ProductoVendido/crear/<int:pk>/',views.producto_vendido_crear,name="productovendido-create"),
    path('ProductoVendido/<int:pk>/edicion/',EdicionProductoVendido.as_view(),name="productovendido-update"),
    path('ProductoVendido/<int:pk>/delete/',views.producto_vendido_delete, name='productovendido-delete'),
    path('ProductoVendido/<int:pk>/delete-edicion/',views.producto_vendido_delete_edicion, name='productovendido-delete-edicion'),
    #PRODUCTO FARMACIA
    path('ProductoFarmacia/', InicioProductoFarmacia.as_view(), name='productofarmacia-inicio'),
    path('ProductoFarmacia/crear/', views.crear_producto_farmacia, name='productofarmacia-create'),
    path('ProductoFarmacia/<int:pk>/edicion/',EdicionProductoFarmacia.as_view(),name="productofarmacia-update"),
    path('ProductoFarmacia/<int:pk>/delete/',views.producto_farmacia_delete, name='productofarmacia-delete'),
]