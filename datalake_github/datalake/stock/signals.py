from django.db.models.signals import pre_save, post_save, pre_delete
from django.contrib.auth.models import User
from django.core.signals import request_finished
from django.dispatch import receiver

from farmacia.models import ProductoVendido
from .models import (
    BodegaVirtual,
    ProductoMermado,
    ProductoIngresado,
)

# Descuenta el stock al ingresar la merma de un producto

@receiver(pre_save, sender=ProductoMermado)
def update_bodega_by_mermado(sender, instance, **kwargs):
    key = instance.nombre.id
    cantidad_mermada = instance.cantidad
    nombre = instance.nombre
    bodvirt = BodegaVirtual.objects.get(nombre_id=key)
    if bodvirt:
        stock_actual = bodvirt.Stock 
        nuevo_stock = stock_actual - cantidad_mermada
        bodvirt.Stock = nuevo_stock
        bodvirt.save()


@receiver(pre_save, sender=ProductoVendido)
def update_bodega_by_venta(sender, instance, **kwargs):
    num = ProductoVendido.objects.filter(pk=instance.pk).count()
    if num == 0:        
        key = instance.nombre.id
        cantidad_vendida = instance.cantidad
        bodvirt = BodegaVirtual.objects.get(nombre_id=key)
        if bodvirt:
            stock_actual = bodvirt.Stock
            nuevo_stock = stock_actual - cantidad_vendida
            bodvirt.Stock = nuevo_stock
            bodvirt.save()
            
    else:
        key = instance.nombre.id
        cantidad_antigua = ProductoVendido.objects.get(pk=instance.pk).cantidad
        cantidad_vendida = instance.cantidad
        cantidad_update = cantidad_vendida - cantidad_antigua
        bodvirt = BodegaVirtual.objects.get(nombre_id=key)
        if bodvirt:
            stock_actual = bodvirt.Stock
            nuevo_stock = stock_actual - cantidad_update
            bodvirt.Stock = nuevo_stock
            bodvirt.save()        

@receiver(pre_delete, sender=ProductoVendido)
def update_bodega_by_venta_ondelete(sender, instance, **kwargs):
        key = instance.nombre.id
        cantidad_vendida_cancelada = instance.cantidad
        bodvirt = BodegaVirtual.objects.get(nombre_id=key)
        if bodvirt:
            stock_actual = bodvirt.Stock
            nuevo_stock = stock_actual + cantidad_vendida_cancelada
            bodvirt.Stock = nuevo_stock
            bodvirt.save()

    
@receiver(pre_save, sender = ProductoIngresado)
def update_bodega_by_ingreso(sender, instance, **kwargs):
    key = instance.nombre.id
    cantidad_ingresada = instance.cantidad
    bodvirt = BodegaVirtual.objects.get(nombre_id=key)
    if bodvirt:
        stock_actual = bodvirt.Stock
        nuevo_stock = stock_actual + cantidad_ingresada
        bodvirt.Stock = nuevo_stock
        bodvirt.save()    



