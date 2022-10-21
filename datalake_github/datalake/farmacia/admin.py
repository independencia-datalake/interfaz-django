from django.contrib import admin
from .models import (
    ProductoFarmacia,
    ProductoVendido,
    ComprobanteVenta,
    CargaProducto,
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
