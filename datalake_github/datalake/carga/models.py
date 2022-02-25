from django.db import models
from core.models import (
    UV,
)

class Empresas(models.Model):
    uv = models.ForeignKey(UV, on_delete=models.PROTECT, verbose_name="Unidad Vecinal")
    rol = models.PositiveIntegerField(verbose_name="ROL",null=True, blank=True)
    razon_social = models.CharField(max_length=60, blank=True, verbose_name="Razon social")
    rut = models.CharField(max_length=200, blank=True, verbose_name="Número de Identidad")
    giro = models.CharField(max_length=60, blank=True, verbose_name="Giro")
    calle = models.CharField(max_length=200, verbose_name="Avenida/Calle/Pasaje",null=True, blank=True)
    numeracion = models.PositiveIntegerField(verbose_name="Numeracion",null=True, blank=True)
    tipo = models.CharField(
        null=True,
        blank=False,
        max_length=200,
        verbose_name='Tipo Patente',
        )
    trabajadores_pais = models.PositiveIntegerField(verbose_name="Trabajadores pais",null=True, blank=True)
    trabajadores_comuna = models.PositiveIntegerField(verbose_name="Trabajadores Comuna",null=True, blank=True)
    trabajadores_patente = models.PositiveIntegerField(verbose_name="Trabajadores Patente",null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación', editable=False)

    class Meta:
        verbose_name = "empresas"
        verbose_name_plural = "empresas"
        ordering = ['created']

class PermisosCirculacion(models.Model):
    uv = models.ForeignKey(UV, on_delete=models.PROTECT, verbose_name="Unidad Vecinal")
    fecha = models.DateField(verbose_name="Fecha",null=True, blank=True)
    calle = models.CharField(blank=True, null=True, max_length=200, verbose_name="Avenida/Calle/Pasaje")
    numero = models.PositiveIntegerField(blank=True, null=True, verbose_name="Numeración")

class LicenciaConducir(models.Model):
    uv = models.ForeignKey(UV, on_delete=models.PROTECT, verbose_name="Unidad Vecinal")
    folio = models.CharField(blank=True, null=True, max_length=200, verbose_name="Folio Licencia")
    calle = models.CharField(blank=True, null=True, max_length=200, verbose_name="Avenida/Calle/Pasaje")
    numero = models.PositiveIntegerField(blank=True, null=True, verbose_name="Numeración")
    comuna = models.CharField(blank=True, null=True, max_length=200, verbose_name="Comuna")
    fecha = models.DateField(verbose_name="Fecha Otorgamiento",null=True, blank=True)

    class Meta:
        verbose_name = "licenciaconducir"
        verbose_name_plural = "licenciasconducir"
        ordering = ['fecha']

class EntregasPandemia(models.Model):
    uv = models.ForeignKey(UV, on_delete=models.PROTECT, verbose_name="Unidad Vecinal")
    n_id = models.CharField(max_length=200, verbose_name="Numero ID",null=True, blank=True)
    fecha = models.DateField(verbose_name="Fecha",null=True, blank=True)
    tipo_identificacion = models.CharField(
        blank=False,
        default='RUT',
        max_length=200,
        choices=(
            ('RUT','Rut'),
            ('PASAPORTE','Pasaporte'),
            ('OTRO','Otro'),
            ),
        verbose_name='Tipo de Documento'
        )
    nombre_persona = models.CharField(max_length=200, verbose_name="Nombre Persona",null=True, blank=True)
    apellido_paterno = models.CharField(max_length=200, verbose_name="Apellido Paterno",null=True, blank=True)
    apellido_materno = models.CharField(max_length=200, verbose_name="Apellido Materno",null=True, blank=True)
    telefono = models.CharField(null=True, blank=True, max_length=200, verbose_name='Teléfono')
    calle = models.CharField(blank=True, null=True, max_length=200, verbose_name="Avenida/Calle/Pasaje")
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
    manzana = models.CharField(null=True, blank=True, max_length=200, verbose_name='Manzana')
    predio = models.CharField(null=True, blank=True, max_length=200, verbose_name='Predio')
    calle = models.CharField(blank=True, null=True, max_length=200, verbose_name="Avenida/Calle/Pasaje")
    numero = models.PositiveIntegerField(blank=True, null=True, verbose_name="Numeración")
    n_permiso = models.CharField(blank=True, null=True, max_length=200, verbose_name="Numero de Permiso")
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación', editable=False)

class ExencionAseo(models.Model):
    uv = models.ForeignKey(UV, on_delete=models.PROTECT, verbose_name="Unidad Vecinal")
    marca_temporal = models.DateTimeField(verbose_name='Marca Temporal',null=True, blank=True)
    tipo_documento = models.CharField(
        blank=False,
        null=True,
        default='RUT',
        max_length=200,
        choices=(
            ('RUT','Rut'),
            ('PASAPORTE','Pasaporte'),
            ('OTRO','Otro'),
            ),
        verbose_name='Tipo de Documento'
        )
    numero_identificacion = models.CharField(null=True, max_length=200, blank=True, verbose_name="Número de Identidad")
    nombres = models.CharField(blank=True, null=True,max_length=200, verbose_name="Nombres")
    apellido_paterno = models.CharField(blank=True, null=True,max_length=200, verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(blank=True, null=True,max_length=200, verbose_name="Apellido Materno")
    estado_civil = models.CharField(blank=True, null=True,max_length=500, verbose_name="Estado Civil")
    ocupacion = models.CharField(blank=True, null=True,max_length=500, verbose_name="Ocupación")
    tramo_rsh = models.PositiveSmallIntegerField(verbose_name='Tramo RSH')
    calle = models.CharField(blank=True, null=True, max_length=500, verbose_name="Avenida/Calle/Pasaje")
    numero = models.PositiveIntegerField(blank=True, null=True, verbose_name="Numeración")
    complemento_direccion = models.CharField(max_length=500, verbose_name='Complemento de Dirección',blank=True,null=True)
    rol_propiedad = models.CharField(blank=True, null=True, max_length=500, verbose_name="Rol Propiedad")
    telefono = models.CharField(null=True, blank=True, max_length=200, verbose_name="Teléfono")
    paga_contribucion = models.CharField(
        null=True,
        blank=False,
        max_length=200,
        choices=(
            ('NO','No'),
            ('SI','Si'),
            ('OTRO','Otro'),
            ),
        verbose_name='Paga Contribucioens'
        )
    porcentaje_exencion = models.PositiveSmallIntegerField(verbose_name="Porcentaje de Exención")
    causal = models.CharField(null=True, blank=True, max_length=200, verbose_name="Causal de Exención")
    adj_docu = models.URLField(max_length=1000, verbose_name="Adjuntar Documentos", null=True, blank=True)
    nombre = models.CharField(blank=True, null=True,max_length=200, verbose_name="Nombres")
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

class CargaLicenciasConducir(models.Model):
    carga_producto = models.FileField(upload_to='carga/patentes_vehiculares/', verbose_name="Patentes Vehiculares")

    def __str__(self):
            return f'Carga Patentes Vehiculares {self.id}' 

class CargaEntregasPandemia(models.Model):
    carga_producto = models.FileField(upload_to='carga/pandemia/', verbose_name="Entrega Pandemia")

    def __str__(self):
            return f'Carga Entrega Pandemia {self.id}' 
