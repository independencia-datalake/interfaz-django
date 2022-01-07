from django.db import models
from core.models import (
    UV,
)

class Empresas(models.Model):
    uv = models.ForeignKey(UV, on_delete=models.PROTECT, verbose_name="Unidad Vecinal")
    rol = models.PositiveIntegerField(verbose_name="ROL")
    razon_social = models.CharField(max_length=60, blank=True, verbose_name="Razon social")
    rut = models.CharField(max_length=30, blank=True, verbose_name="Número de Identidad")
    giro = models.CharField(max_length=60, blank=True, verbose_name="Giro")
    calle = models.CharField(max_length=30, verbose_name="Avenida/Calle/Pasaje")
    numeracion = models.PositiveIntegerField(verbose_name="Numeracion")
    tipo = models.CharField(
        null=True,
        blank=False,
        max_length=30,
        verbose_name='Tipo Patente'
        )
    trabajadores_pais = models.PositiveIntegerField(verbose_name="Trabajadores pais")
    trabajadores_comuna = models.PositiveIntegerField(verbose_name="Trabajadores Comuna")
    trabajadores_patente = models.PositiveIntegerField(verbose_name="Trabajadores Patente")
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación', editable=False)

    class Meta:
        verbose_name = "empresas"
        verbose_name_plural = "empresas"
        ordering = ['created']

class PermisosCirculacion(models.Model):
    uv = models.ForeignKey(UV, on_delete=models.PROTECT, verbose_name="Unidad Vecinal")
    fecha = models.DateField(verbose_name="Fecha")
    rut = models.CharField(max_length=30, blank=True, verbose_name="Número de Identidad")
    nombres = models.CharField(max_length=30, blank=True, verbose_name="Nombres")
    efectuo_tramite = models.CharField(max_length=30, blank=True, verbose_name="Efectuo Tramite")

class PatentesVehiculares(models.Model):
    uv = models.ForeignKey(UV, on_delete=models.PROTECT, verbose_name="Unidad Vecinal")
    año_fabricacion = models.PositiveIntegerField(verbose_name="Trabajadores pais")
    marca = models.CharField(max_length=30, verbose_name="Marca del auto")
    placa = models.CharField(max_length=30, verbose_name="Placa")
    calle =models.CharField(max_length=30, verbose_name="Avenida/Calle/Pasaje")
    numeracion = models.PositiveIntegerField(verbose_name="Numeracion")
    modelo = models.CharField(max_length=30, verbose_name="Modelo del auto")
    color = models.CharField(max_length=30, verbose_name="Color")
    codigo_sii = models.CharField(max_length=30, verbose_name="Codigo de SII")
    forma_pago = models.CharField(
        null=True,
        blank=False,
        default='',
        max_length=30,
        choices=(
            ('1RA CUOTA','1er cuota'),
            ('2DA CUOTA','2da cuota'),
            ('CONTADO','Contado'),
            ('OTRO','Otro'),
            ),
        verbose_name='Forma de pago'
        )
    total_pagar = models.PositiveIntegerField(verbose_name="Total a Pagar")
    año_permiso = models.PositiveIntegerField(verbose_name="Año de Permiso")
    fecha_pago = models.DateField(verbose_name="fecha de Pago")

    class Meta:
        verbose_name = "patentesvehiculares"
        verbose_name_plural = "patentesvehiculares"
        ordering = ['fecha_pago']

class EntregasPandemia(models.Model):
    uv = models.ForeignKey(UV, on_delete=models.PROTECT, verbose_name="Unidad Vecinal")
    n_id = models.PositiveIntegerField(verbose_name="Número ID")
    fecha = models.DateField(verbose_name="Fecha")
    tipo_identificacion = models.CharField(
        blank=False,
        default='RUT',
        max_length=30,
        choices=(
            ('RUT','Rut'),
            ('PASAPORTE','Pasaporte'),
            ('OTRO','Otro'),
            ),
        verbose_name='Tipo de Documento'
        )
    nombre_persona = models.CharField(max_length=30, verbose_name="Nombre Persona")
    apellido_paterno = models.CharField(max_length=30, verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(max_length=30, verbose_name="Apellido Materno")
    telefono = models.CharField(null=True, blank=True, max_length=30, verbose_name='Teléfono')
    calle = models.CharField(blank=True, null=True, max_length=30, verbose_name="Avenida/Calle/Pasaje")
    numero = models.PositiveIntegerField(blank=True, null=True, verbose_name="Numeración")
    complemento_direccion = models.CharField(max_length=50, verbose_name='Complemento de Dirección',blank=True,null=True)
    caja_mercaderia = models.PositiveIntegerField(blank=True, null=True, verbose_name="Caja Mercaderia")
    pañal_adulto = models.PositiveIntegerField(blank=True, null=True, verbose_name="Pañal Adulto")
    pañal_niño_m = models.PositiveIntegerField(blank=True, null=True, verbose_name="Pañal niño talla M")
    pañal_niño_g = models.PositiveIntegerField(blank=True, null=True, verbose_name="Pañal niño talla G")
    pañal_niño_xg = models.PositiveIntegerField(blank=True, null=True, verbose_name="Pañal niño talla XG")
    pañal_niño_xxg = models.PositiveIntegerField(blank=True, null=True, verbose_name="Pañal niño talla XXG")
    leche_entera = models.PositiveIntegerField(blank=True, null=True, verbose_name="Leche entera")
    leche_descremada = models.PositiveIntegerField(blank=True, null=True, verbose_name="Leche descremada")
    nat_100 = models.PositiveIntegerField(blank=True, null=True, verbose_name="NAT 100")
    balon_gas = models.PositiveIntegerField(blank=True, null=True, verbose_name="Balon de gas 11 kg")
    parafina = models.PositiveIntegerField(blank=True, null=True, verbose_name="Parafina")
    
class DOM(models.Model):
    uv = models.ForeignKey(UV, on_delete=models.PROTECT, verbose_name="Unidad Vecinal")
    tramite = models.CharField(null=True, blank=True, max_length=60, verbose_name='Tramite')
    manzana = models.CharField(null=True, blank=True, max_length=30, verbose_name='Manzana')
    predio = models.CharField(null=True, blank=True, max_length=30, verbose_name='Predio')
    calle = models.CharField(blank=True, null=True, max_length=30, verbose_name="Avenida/Calle/Pasaje")
    numero = models.PositiveIntegerField(blank=True, null=True, verbose_name="Numeración")
    n_permiso = models.CharField(blank=True, null=True, max_length=30, verbose_name="Numero de Permiso")
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación', editable=False)

class ExencionAseo(models.Model):
    uv = models.ForeignKey(UV, on_delete=models.PROTECT, verbose_name="Unidad Vecinal")
    marca_temporal = models.DateTimeField(verbose_name='Marca Temporal')
    tipo_documento = models.CharField(
        blank=False,
        default='RUT',
        max_length=30,
        choices=(
            ('RUT','Rut'),
            ('PASAPORTE','Pasaporte'),
            ('OTRO','Otro'),
            ),
        verbose_name='Tipo de Documento'
        )
    numero_identificacion = models.CharField(null=True, max_length=30, blank=True, verbose_name="Número de Identidad")
    nombres = models.CharField(blank=True, null=True,max_length=30, verbose_name="Nombres")
    apellido_paterno = models.CharField(blank=True, null=True,max_length=30, verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(blank=True, null=True,max_length=30, verbose_name="Apellido Materno")
    estado_civil = models.CharField(blank=True, null=True,max_length=30, verbose_name="Estado Civil")
    ocupacion = models.CharField(blank=True, null=True,max_length=30, verbose_name="Ocupación")
    tramo_rsh = models.PositiveSmallIntegerField(verbose_name='Tramo RSH')
    calle = models.CharField(blank=True, null=True, max_length=30, verbose_name="Avenida/Calle/Pasaje")
    numero = models.PositiveIntegerField(blank=True, null=True, verbose_name="Numeración")
    complemento_direccion = models.CharField(max_length=50, verbose_name='Complemento de Dirección',blank=True,null=True)
    rol_propiedad = models.CharField(blank=True, null=True, max_length=50, verbose_name="Rol Propiedad")
    telefono = models.CharField(null=True, blank=True, max_length=30, verbose_name="Teléfono")
    paga_contribucion = models.CharField(
        null=True,
        blank=False,
        max_length=5,
        choices=(
            ('NO','No'),
            ('SI','Si'),
            ('OTRO','Otro'),
            ),
        verbose_name='Paga Contribucioens'
        )
    porcentaje_exencion = models.PositiveSmallIntegerField(verbose_name="Porcentaje de Exención")
    causal = models.CharField(null=True, blank=True, max_length=200, verbose_name="Causal de Exención")
    adj_docu = models.URLField(max_length=200, verbose_name="Adjuntar Documentos")
    nombre = models.CharField(blank=True, null=True,max_length=30, verbose_name="Nombres")
    serie = models.PositiveIntegerField(verbose_name="Serie")

class CargaDOM(models.Model):
    carga_producto = models.FileField(upload_to='carga/DOM/', verbose_name="Dom - Tramites y permisos")

    def __str__(self):
            return f'Carga DOM {self.id}'

class CargaExencionAseo(models.Model):
    carga_producto = models.FileField(upload_to='carga/exencion_aseo/', verbose_name="Exención pago derechos de aseo")

    def __str__(self):
            return f'Carga exención pago derechos de aseo {self.id}'  

class CargaEmpresas(models.Model):
    carga_producto = models.FileField(upload_to='carga/empresas/', verbose_name="Empresas")

    def __str__(self):
            return f'Carga Empresas {self.id}' 

class CargaPermisosCirculacion(models.Model):
    carga_producto = models.FileField(upload_to='carga/permiso_circulacion/', verbose_name="Permisos Circulacion")

    def __str__(self):
            return f'Carga Permisos Circulacion {self.id}' 

class CargaPatentesVehiculares(models.Model):
    carga_producto = models.FileField(upload_to='carga/patentes_vehiculares/', verbose_name="Patentes Vehiculares")

    def __str__(self):
            return f'Carga Patentes Vehiculares {self.id}' 

class CargaEntregasPandemia(models.Model):
    carga_producto = models.FileField(upload_to='carga/pandemia/', verbose_name="Entrega Pandemia")

    def __str__(self):
            return f'Carga Entrega Pandemia {self.id}' 