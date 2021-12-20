from django.db import models
from core.models import (
    UV,
    obtener_uv,
)

class Empresas(models.Model):
    carga_producto = models.FileField(upload_to='carga/empresas/', verbose_name="Empresas")
    # uv = models.ForeignKey(UV, on_delete=models.PROTECT, verbose_name="Unidad Vecinal")
    # rol = models.PositiveIntegerField(verbose_name="ROL")
    # razon_social = models.CharField(max_length=60, blank=True, verbose_name="Razon social")
    # rut = models.CharField(max_length=30, blank=True, verbose_name="Número de Identidad")
    # giro = models.CharField(max_length=60, blank=True, verbose_name="Giro")
    # calle = models.CharField(max_length=30, verbose_name="Avenida/Calle/Pasaje")
    # numeracion = models.PositiveIntegerField(verbose_name="Numeracion")
    # tipo = models.CharField(
    #     null=True,
    #     blank=False,
    #     default='',
    #     max_length=30,
    #     choices=(
    #         ('ALCOHOL','Alcohol'),
    #         ('COMERCIAL','Comercial'),
    #         ('ESTACIONADO','Estacionado'),
    #         ('INDUSTRIAL','Industrial'),
    #         ('MICROEMPRESA','Microempresa'),
    #         ('PROFESIONAL','Profesional'),
    #         ),
    #     verbose_name='Tipo Patente'
    #     )
    # trabajadores_pais = models.PositiveIntegerField(verbose_name="Trabajadores pais")
    # trabajadores_comuna = models.PositiveIntegerField(verbose_name="Trabajadores Comuna")
    # trabajadores_patente = models.PositiveIntegerField(verbose_name="Trabajadores Patente")

    # def save(self, *args, **kwargs):
    #     uv = obtener_uv(self.calle,self.numeracion)
    #     self.uv = UV.objects.get(numero_uv=uv)
    #     return super(Empresas, self).save(*args, **kwargs)

class PermisosCirculacion(models.Model):
    carga_producto = models.FileField(upload_to='carga/permiso_circulacion/', verbose_name="Permisos Circulacion")
    # fecha = models.DateField(verbose_name="Fecha")
    # rut = models.CharField(max_length=30, blank=True, verbose_name="Número de Identidad")
    # nombres = models.CharField(max_length=30, blank=True, verbose_name="Nombres")
    # efectuo_tramite = models.CharField(max_length=30, blank=True, verbose_name="Efectuo Tramite")

class PatentesVehiculares(models.Model):
    carga_producto = models.FileField(upload_to='carga/patentes_vehiculares/', verbose_name="Patentes Vehiculares")
    # año_fabricacion = models.PositiveIntegerField(verbose_name="Trabajadores pais")
    # marca = models.CharField(max_length=30, verbose_name="Marca del auto")
    # placa = models.CharField(max_length=30, verbose_name="Placa")
    # calle =models.CharField(max_length=30, verbose_name="Avenida/Calle/Pasaje")
    # numeracion = models.PositiveIntegerField(verbose_name="Numeracion")
    # modelo = models.CharField(max_length=30, verbose_name="Modelo del auto")
    # color = models.CharField(max_length=30, verbose_name="Color")
    # codigo_sii = models.CharField(max_length=30, verbose_name="Codigo de SII")
    # forma_pago = models.CharField(
    #     null=True,
    #     blank=False,
    #     default='',
    #     max_length=30,
    #     choices=(
    #         ('1RA CUOTA','1er cuota'),
    #         ('2DA CUOTA','2da cuota'),
    #         ('CONTADO','Contado'),
    #         ('OTRO','Otro'),
    #         ),
    #     verbose_name='Forma de pago'
    #     )
    # total_pagar = models.PositiveIntegerField(verbose_name="Total a Pagar")
    # año_permiso = models.PositiveIntegerField(verbose_name="Año de Permiso")
    # fecha_pago = models.DateField(verbose_name="fecha de Pago")

class EntregasPandemia(models.Model):
    carga_producto = models.FileField(upload_to='carga/pandemia/', verbose_name="Entrega Pandemia")
    # n_id = models.PositiveIntegerField(verbose_name="Número ID")
    # fecha = models.DateField(verbose_name="Fecha")
    # tipo_identificacion = models.CharField(
    #     blank=False,
    #     default='RUT',
    #     max_length=30,
    #     choices=(
    #         ('RUT','Rut'),
    #         ('PASAPORTE','Pasaporte'),
    #         ('OTRO','Otro'),
    #         ),
    #     verbose_name='Tipo de Documento'
    #     )
    # nombre_persona = models.CharField(max_length=30, verbose_name="Nombre Persona")
    # apellido_paterno = models.CharField(max_length=30, verbose_name="Apellido Paterno")
    # apellido_materno = models.CharField(max_length=30, verbose_name="Apellido Materno")
    # telefono = models.CharField(null=True, blank=True, max_length=30, verbose_name='Teléfono')
    # calle = models.CharField(blank=True, null=True, max_length=30, verbose_name="Avenida/Calle/Pasaje")
    # numero = models.PositiveIntegerField(blank=True, null=True, verbose_name="Numeración")
    # complemento_direccion = models.CharField(max_length=50, verbose_name='Complemento de Dirección',blank=True,null=True)
    # uv = models.ForeignKey(UV, on_delete=models.PROTECT, verbose_name="Unidad Vecinal")
    # caja_mercaderia = models.PositiveIntegerField(blank=True, null=True, verbose_name="Caja Mercaderia")
    # pañal_adulto = models.PositiveIntegerField(blank=True, null=True, verbose_name="Pañal Adulto")
    # pañal_niño_m = models.PositiveIntegerField(blank=True, null=True, verbose_name="Pañal niño talla M")
    # pañal_niño_g = models.PositiveIntegerField(blank=True, null=True, verbose_name="Pañal niño talla G")
    # pañal_niño_xg = models.PositiveIntegerField(blank=True, null=True, verbose_name="Pañal niño talla XG")
    # pañal_niño_xxg = models.PositiveIntegerField(blank=True, null=True, verbose_name="Pañal niño talla XXG")
    # leche_entera = models.PositiveIntegerField(blank=True, null=True, verbose_name="Leche entera")
    # leche_descremada = models.PositiveIntegerField(blank=True, null=True, verbose_name="Leche descremada")
    # nat_100 = models.PositiveIntegerField(blank=True, null=True, verbose_name="NAT 100")
    # balon_gas = models.PositiveIntegerField(blank=True, null=True, verbose_name="Balon de gas 11 kg")
    # parafina = models.PositiveIntegerField(blank=True, null=True, verbose_name="Parafina")