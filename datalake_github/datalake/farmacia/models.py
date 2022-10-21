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
    f_ven = models.DateField(auto_now_add=False, auto_now=False, verbose_name="Fecha de vencimiento",null=True, blank=True)
    precio = models.PositiveIntegerField(default=1, verbose_name="Precio Producto",null=True, blank=True)
    n_lote = models.CharField(max_length=200, verbose_name="Lote",null=True, blank=True)
    bioequivalencia = models.BooleanField(verbose_name = "Bioequivalencia",null=True, blank=True)
    cenabast = models.BooleanField(verbose_name = "Cenabast",null=True, blank=True)
    
    autor = models.ForeignKey(User, on_delete=models.PROTECT, null=True)     
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)

    class Meta:
        verbose_name = "Producto Farmacia"
        verbose_name_plural = "Productos de Farmacia"
        ordering = ['marca_producto','dosis']

    def __str__(self):
        return f'{self.marca_producto} {self.p_a} {self.dosis} {self.presentacion} | Lote: {self.n_lote} | Precio: ${self.precio} '

    def  get_absolute_url(self):
        return reverse("productofarmacia-inicio")  

class ComprobanteVenta(models.Model):
    comprador = models.ForeignKey(Persona, on_delete=models.PROTECT,verbose_name='Comprador') 
    receta = models.FileField(blank=True, null=True,upload_to='farmacia/receta_medica/%Y/%m/%d/')
    
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

class CargaProducto(models.Model):
    carga_producto = models.FileField(blank=True, null=True, upload_to='farmacia/carga_producto/')

    def __str__(self):
        return f'carga numero {self.id}'

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

