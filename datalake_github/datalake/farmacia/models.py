from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class ProductoFarmacia(models.Model): 
    marca_producto = models.CharField(max_length=20, verbose_name="Marca del Producto")
    p_a =  models.CharField(max_length=20, verbose_name="Componente Activo")
    dosis = models.CharField(max_length=10, verbose_name="Dosis del Producto")
    precentacion = models.CharField(max_length=10, verbose_name="Precentacion del Producto")
    f_ven = models.DateTimeField(auto_now_add=False, auto_now=False, verbose_name="Fecha de vencimiento")
    precio = models.PositiveIntegerField(default=1, verbose_name="Precio Producto")
    n_lote = models.PositiveIntegerField(default=1, verbose_name="Numero de Lote")
    
    autor = models.ForeignKey(User, on_delete=models.PROTECT, null=True)     
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)

    class Meta:
        verbose_name = "Producto Farmacia"
        verbose_name_plural = "Productos de Farmacia"
        ordering = ['p_a','dosis']

    def __str__(self):
        return f'{self.marca_producto} {self.p_a} {self.dosis} {self.precentacion} | Lote: {self.n_lote} | Precio: ${self.precio} '

    def  get_absolute_url(self):
        return reverse("productofarmacia-inicio")  

class ComprobanteVenta(models.Model): 
    tipo_identificacion = models.CharField(blank=False, default='Rut', max_length=30,
                                            choices=(
                                                ('Rut','Rut'),
                                                ('Pasaporte','Pasaporte'),
                                                ('Otro','Otro'),
                                            )
                                          )    
    numero_identificacion = models.CharField(max_length=30, blank=True, verbose_name="Numero de Identidad")
    
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
