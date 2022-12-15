from django.contrib import admin


from .models import (
    BodegaVirtual,
    OrdenIngresoProducto,
    OrdenIngresoList,
    ProductoIngresado,
    ProductoMermado,
)

class OrdenIngresoProductoAdmin(admin.ModelAdmin):
    readonly_fields = ['created','updated']

class ProductoIngresadoAdmin(admin.ModelAdmin):
    readonly_fields = ['created','updated']

admin.site.register(BodegaVirtual) 
admin.site.register(OrdenIngresoProducto)
admin.site.register(OrdenIngresoList)
admin.site.register(ProductoIngresado)  
admin.site.register(ProductoMermado)  
# Register your models here.
