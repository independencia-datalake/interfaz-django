from django.contrib import admin
from .models import (
    BodegaVirtual,
    Laboratorios,
    OrdenIngresoProducto,
    ProductoIngresado,
)

class OrdenIngresoProductoAdmin(admin.ModelAdmin):
    readonly_fields = ['created','updated']

class ProductoIngresadoAdmin(admin.ModelAdmin):
    readonly_fields = ['created','updated']

admin.site.register(BodegaVirtual) 
admin.site.register(Laboratorios) 
admin.site.register(OrdenIngresoProducto)
admin.site.register(ProductoIngresado)  
# Register your models here.
