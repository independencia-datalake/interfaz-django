from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import(
    Persona,
)
from .validators import (
    validacion_de_palabras,
)

class ProductoFarmacia(models.Model): 
    active = models.BooleanField(default=True, verbose_name="Activo",null=True)
    marca_producto = models.CharField(max_length=200, verbose_name="Nombre del Producto",null=True)
    p_a =  models.CharField(max_length=200, verbose_name="Componente Activo",null=True)
    dosis = models.CharField(max_length=200, verbose_name="Dosis del Producto",null=True)
    presentacion = models.CharField(max_length=200, verbose_name="Presentacion del Producto",null=True)
    f_ven = models.DateField(auto_now_add=False, auto_now=False, verbose_name="Fecha de vencimiento",null=True)
    precio = models.PositiveIntegerField(default=1, verbose_name="Precio Producto",null=True)
    n_lote = models.CharField(max_length=200, verbose_name="Lote",null=True)
    
    autor = models.ForeignKey(User, on_delete=models.PROTECT, null=True)     
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)

    class Meta:
        verbose_name = "Producto Farmacia"
        verbose_name_plural = "Productos de Farmacia"
        ordering = ['p_a','dosis']

    def __str__(self):
        return f'{self.marca_producto} {self.p_a} {self.dosis} {self.presentacion} | Lote: {self.n_lote} | Precio: ${self.precio} '

    def  get_absolute_url(self):
        return reverse("productofarmacia-inicio")  

class ComprobanteVenta(models.Model):
    comprador = models.ForeignKey(Persona, on_delete=models.PROTECT,verbose_name='Comprador') 
    # tipo_identificacion = models.CharField(blank=False, default='RUT', max_length=30,
    #                                         choices=(
    #                                             ('RUT','Rut'),
    #                                             ('PASAPORTE','Pasaporte'),
    #                                             ('OTRO','Otro'),
    #                                         ),verbose_name='Tipo de Documento'
    #                                       )    
    # numero_identificacion = models.CharField(max_length=30, blank=False, verbose_name="Número de Identidad")
    receta = models.ImageField(default='default.jpg', blank=True, null=True, upload_to='receta_medica')
    
    farmaceuta = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Profesional')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)

    class Meta:
        verbose_name = "Comprobante Venta"
        verbose_name_plural = "Comprobantes de Venta"

    def __str__(self):
        return f'{self.pk}'
    
    def  get_absolute_url(self):
        return reverse("comprobanteventa-detail", kwargs={"pk": self.pk})


class ProductoVendido(models.Model):
    nombre = models.ForeignKey(ProductoFarmacia, on_delete=models.PROTECT, verbose_name="Nombre Producto")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad Vendida")

    n_venta = models.ForeignKey(ComprobanteVenta, on_delete=models.CASCADE)
    
    farmaceuta = models.ForeignKey(User, on_delete=models.PROTECT) 
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)

    class Meta:
        verbose_name = "Producto Vendido"
        verbose_name_plural = "Productos Vendidos"
        ordering = ['-n_venta']
    
    def __str__(self):
        return f'{self.n_venta} - {self.nombre} - {self.cantidad}'

    def  get_absolute_url(self):
        return reverse("comprobanteventa-detail", kwargs={"pk": self.n_venta})

