from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import(
    Persona,
)
from farmacia.models import(
    ProductoFarmacia
)


# Create your models here.

class BodegaVirtual(models.Model):
    nombre = models.ForeignKey(ProductoFarmacia, on_delete=models.PROTECT, verbose_name="Nombre Producto")
    Stock = models.IntegerField(null=True, blank=True, verbose_name="Stock del producto")
    Stock_min =  models.IntegerField(null=True, blank=True,verbose_name="Stock minimo del producto")
    Stock_max = models.IntegerField(null=True, blank=True,verbose_name="Stock maximo del producto")
    holgura = models.IntegerField(null=True, blank=True,verbose_name="Holgura del Stock")

    def __str__(self):
        return f'{self.nombre} '
    class Meta:
        verbose_name= "Bodega Virtual"
        verbose_name_plural = "Bodega Virtual"
        db_table = "BodegaVirtual"
    def save(self, *args, **kwargs):
        self.holgura = self.Stock - self.Stock_min
        return super(BodegaVirtual, self).save(*args, **kwargs)    
    def  get_absolute_url(self):
        return reverse("Stock-inicio")  

class Laboratorios(models.Model):
    nombre_laboratorio = models.CharField(max_length=50, verbose_name="Nombre del Laboratorio",null=True, blank=True)

    class Meta:
        verbose_name = "Laboratorio"
        verbose_name_plural = "Laboratorios"
    def __str__(self):
        return f'{self.nombre_laboratorio}'
    
   
class OrdenIngresoProducto(models.Model):
    estado = models.BooleanField(default = False, verbose_name = "Estado Ingreso",null=True, blank=True)
    farmaceuta = models.ForeignKey(User,null=True, blank=True, on_delete=models.PROTECT, verbose_name='Profesional')

    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)
    class Meta:
        verbose_name = "Orden de Ingreso de Producto"
        verbose_name_plural = "Ordenes de Ingresos de Productos"
    def __str__(self):
        return f'{self.id}'

class ProductoIngresado(models.Model):
    nombre = models.ForeignKey(ProductoFarmacia, on_delete=models.PROTECT, verbose_name="Nombre Producto")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad Ingresada al Stock")
    laboratorio = models.ForeignKey(Laboratorios, on_delete=models.PROTECT, verbose_name="Laboratorio")
    precio_compra = models.PositiveIntegerField(default=0, verbose_name="Precio Compra Producto",null=True, blank=True)
    n_venta = models.ForeignKey(OrdenIngresoProducto, on_delete=models.CASCADE)
    cenabast = models.BooleanField(default = False, verbose_name = "Cenabast",null=True, blank=True)
    
    proveedor = models.CharField(max_length=25, verbose_name="Proveedor",null=True, blank=True) #todo eliminar?????????????
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)

    class Meta:
        verbose_name = "Producto Ingresado"
        verbose_name_plural = "Productos Ingresados"
        ordering = ['-n_venta']
    
    def __str__(self):
        return f'{self.n_venta} - {self.nombre} || Cantidad Ingresada:  {self.cantidad}'

    def  get_absolute_url(self):
        return reverse("comprobanteventa-detail", kwargs={"pk": self.n_venta}) #!ojo aca

class ProductoMermado(models.Model):
    nombre = models.ForeignKey(ProductoFarmacia, on_delete=models.PROTECT, verbose_name="Nombre Producto")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad Mermada")
    farmaceuta = models.ForeignKey(User, on_delete=models.PROTECT)  
    motivo = models.CharField(max_length=100, verbose_name="Motivo",null=True, blank=True) 
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)

    class Meta:
        verbose_name = "Producto Mermado"
        verbose_name_plural = "Productos Mermados"
    
    def __str__(self):
        return f'{self.nombre} - {self.cantidad} - {self.created}'

    def  get_absolute_url(self):
        return reverse("Stock-home")  
