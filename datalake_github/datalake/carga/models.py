from django.db import models
from core.models import (
    UV,
    obtener_uv,
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
        default='',
        max_length=30,
        choices=(
            ('ALCOHOL','Alcohol'),
            ('COMERCIAL','Comercial'),
            ('ESTACIONADO','Estacionado'),
            ('INDUSTRIAL','Industrial'),
            ('MICROEMPRESA','Microempresa'),
            ('PROFESIONAL','Profesional'),
            ),
        verbose_name='Tipo Patente'
        )
    trabajadores_pais = models.PositiveIntegerField(verbose_name="Trabajadores pais")
    trabajadores_comuna = models.PositiveIntegerField(verbose_name="Trabajadores Comuna")
    trabajadores_patente = models.PositiveIntegerField(verbose_name="Trabajadores Patente")

    def save(self, *args, **kwargs):
        uv = obtener_uv(self.calle,self.numeracion)
        self.uv = UV.objects.get(numero_uv=uv)
        return super(Empresas, self).save(*args, **kwargs)

class PermisosCirculacion(models.Model):
    fecha = models.DateField(verbose_name="Fecha")
    rut = models.CharField(max_length=30, blank=True, verbose_name="Número de Identidad")
    nombres = models.CharField(max_length=30, blank=True, verbose_name="Nombres")
    efectuo_tramite = models.CharField(max_length=30, blank=True, verbose_name="Efectuo Tramite")

class PatentesVehiculares(models.Model):
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