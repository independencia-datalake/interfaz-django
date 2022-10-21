from django.contrib import admin
from .models import (
    ProductoFarmacia,
    ProductoVendido,
    ComprobanteVenta,
    CargaProducto,
    BodegaVirtual,
    Laboratorios,
    OrdenIngresoProducto,
    ProductoIngresado,
)

class ProductoFarmaciaAdmin(admin.ModelAdmin):
    readonly_fields = ['created','updated']

class ProductoVendidoAdmin(admin.ModelAdmin):
    readonly_fields = ['created','updated']

class ComprobanteVentaAdmin(admin.ModelAdmin):
    readonly_fields = ['created','updated']


admin.site.register(ProductoFarmacia, ProductoFarmaciaAdmin)
admin.site.register(ProductoVendido, ProductoVendidoAdmin)
admin.site.register(ComprobanteVenta, ComprobanteVentaAdmin) 
admin.site.register(CargaProducto) 
admin.site.register(BodegaVirtual) 
admin.site.register(Laboratorios) 
admin.site.register(OrdenIngresoProducto)
admin.site.register(ProductoIngresado)  