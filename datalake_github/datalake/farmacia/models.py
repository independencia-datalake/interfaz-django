from email.policy import default
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import(
    Persona,
)

class ProductoFarmacia(models.Model): 

    active = models.BooleanField(default=True, verbose_name="Activo",null=True, blank=True)
    marca_producto = models.CharField(max_length=200, verbose_name="Nombre del Producto",null=True, blank=True)
    p_a =  models.CharField(max_length=200, verbose_name="Componente Activo",null=True, blank=True)
    dosis = models.CharField(max_length=200, verbose_name="Dosis del Producto",null=True, blank=True)
    presentacion = models.CharField(max_length=200, verbose_name="Presentacion del Producto",null=True, blank=True)
    precio = models.PositiveIntegerField(default=1, verbose_name="Precio Producto",null=True, blank=True)
    bioequivalencia = models.BooleanField(default = False, verbose_name = "Bioequivalencia",null=True, blank=True)
    
    autor = models.ForeignKey(User, on_delete=models.PROTECT, null=True)     
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)

    class Meta:
        verbose_name = "Producto Farmacia"
        verbose_name_plural = "Productos de Farmacia"
        ordering = ['marca_producto','dosis']

    def __str__(self):
        return f'{self.marca_producto} | Precio: ${self.precio} '

    def  get_absolute_url(self):
        return reverse("productofarmacia-inicio")  

class ComprobanteVenta(models.Model):
    comprador = models.ForeignKey(Persona, on_delete=models.PROTECT,verbose_name='Comprador') 
    receta = models.FileField(blank=True, null=True,upload_to='farmacia/receta_medica/%Y/%m/%d/')
    
    farmaceuta = models.ForeignKey(User,null = True , blank=True, on_delete=models.PROTECT, verbose_name='Profesional')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)

    class Meta:
        verbose_name = "Comprobante Venta"
        verbose_name_plural = "Comprobantes de Venta"

    def __str__(self):
        return f'{self.pk}'
    
    def  get_absolute_url(self):
        return reverse("comprobanteventa-detail", kwargs={"pk": self.pk})

class Recetas(models.Model):
    receta = models.FileField(blank=True, null=True,upload_to='farmacia/receta_medica/%Y/%m/%d/')
    comprobante_venta = models.ForeignKey(ComprobanteVenta, on_delete=models.PROTECT, verbose_name="Venta asociada")

    class Meta:
        verbose_name = "Receta Medica"
        verbose_name_plural = "Recetas Medicas"
    def __str__(self):
        return f'Receta N°:  {self.pk} || Asociada a Venta N°:  {self.comprobante_venta}'

class ProductoVendido(models.Model):
    nombre = models.ForeignKey(ProductoFarmacia, on_delete=models.PROTECT, verbose_name="Nombre Producto")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad Vendida")
    precio_venta = models.PositiveIntegerField(verbose_name="Precio Producto de la Venta",null=True, blank=True)
    n_venta = models.ForeignKey(ComprobanteVenta, on_delete=models.CASCADE)
    

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

class CargaProducto(models.Model):
    carga_producto = models.FileField(blank=True, null=True, upload_to='farmacia/carga_producto/')

    def __str__(self):
        return f'carga numero {self.id}'


