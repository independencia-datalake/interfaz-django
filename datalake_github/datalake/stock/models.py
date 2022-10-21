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
    # def _get_total(self):
    #     "Returns the total"
    #     return self.Stock - self.Stock_min
    # holgura = property(_get_total)

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

# def save(self, *args, **kargs):
#         self.holgura = self.stock - self.stock_min
#         return super(BodegaVirtual, *args).save()

class Laboratorios(models.Model):
    nombre_laboratorio = models.CharField(max_length=50, verbose_name="Nombre del Laboratorio",null=True, blank=True)

    class Meta:
        verbose_name = "Laboratorio"
        verbose_name_plural = "Laboratorios"
    def __str__(self):
        return f'{self.nombre_laboratorio}'
    
   
class OrdenIngresoProducto(models.Model):
    nombre = models.ForeignKey(ProductoFarmacia, on_delete=models.PROTECT, verbose_name="Nombre Producto")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)
    class Meta:
        verbose_name = "Orden de Ingreso de Producto"
        verbose_name_plural = "Ordenes de Ingresos de Productos"
    def __str__(self):
        return f'{self.nombre}'

class ProductoIngresado(models.Model):
    nombre = models.ForeignKey(ProductoFarmacia, on_delete=models.PROTECT, verbose_name="Nombre Producto")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad Vendida")
    laboratorio = models.ForeignKey(Laboratorios, on_delete=models.PROTECT, verbose_name="Nombre Producto")

    n_venta = models.ForeignKey(OrdenIngresoProducto, on_delete=models.CASCADE)
    
    proveedor = models.CharField(max_length=25, verbose_name="Proveedor",null=True, blank=True) #todo eliminar?????????????
    farmaceuta = models.ForeignKey(User, on_delete=models.PROTECT)  #todo eliminar?????????????
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)

    class Meta:
        verbose_name = "Producto Ingresado"
        verbose_name_plural = "Productos Ingresados"
        ordering = ['-n_venta']
    
    def __str__(self):
        return f'{self.n_venta} - {self.nombre} - {self.cantidad}'

    def  get_absolute_url(self):
        return reverse("comprobanteventa-detail", kwargs={"pk": self.n_venta}) #!ojo aca