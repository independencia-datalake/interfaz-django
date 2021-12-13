from django.contrib.auth.models import User
from django.db import models
from django.db.models.base import Model
from core.models import (
    obtener_uv,
    UV,
)


class ClasificacionDelito(models.Model):
    nombre = models.CharField(max_length=40, verbose_name='Clasificacion de delito')

    class Meta:
        verbose_name = "Clasificación del delito"
        verbose_name_plural = "Clasificaciones de los delitos"
        ordering = ['id']
        
    def __str__(self):
        return f'{self.nombre}'

class Delito(models.Model):
    clasificacion_delito = models.ForeignKey(ClasificacionDelito, on_delete=models.PROTECT, verbose_name='Clasificacion del delito')
    nombre = models.CharField(max_length=200, verbose_name='Delito')
    
    class Meta:
        verbose_name = "Delito"
        verbose_name_plural = "Delitos"
        ordering = ['clasificacion_delito','id']
        
    def __str__(self):
        return f'{self.nombre}'

class LlamadoSeguridad(models.Model):
    numero_requerimiento = models.AutoField(primary_key=True, verbose_name='Número de requerimiento')
    fecha_ingreso = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de ingreso", editable=False)

    class Meta:
        verbose_name = "Llamado seguridad"
        verbose_name_plural = "Llamados de seguridad"
        ordering = ['numero_requerimiento']
        
    def __str__(self):
        return f'{self.numero_requerimiento}'

class Denunciante(models.Model):
    nombre = models.CharField(null=True, blank=True, max_length=30,verbose_name='Nombre')
    apellido = models.CharField(null=True, blank=True, max_length=30,verbose_name='Apellido')
    telefono = models.CharField(null=True, blank=True, max_length=30,verbose_name='Teléfono denunciante')
    correo = models.EmailField(null=True, blank=True, max_length=40, verbose_name="Correo electrónico")

    class Meta:
        verbose_name = "Denunciante"
        verbose_name_plural = "Denunciantes"
        ordering = ['id']
        
    def __str__(self):
        return f'{self.nombre}'

class Requerimiento(models.Model):
    numero_requerimiento = models.ForeignKey(LlamadoSeguridad, on_delete=models.CASCADE, verbose_name='Número de requerimiento')
    uv = models.ForeignKey(UV, on_delete=models.PROTECT, verbose_name='Unidad Vecinal')
    estatus = models.CharField(
        max_length=1,
        default='1',
        choices=(
            ('1','Recepcionado'),
            ('2','Pendiente'),
            ('3','En Curso'),
            ('4','Resuelto'),
            ),
        verbose_name='Estatus',
        )
    via_ingreso = models.CharField(
        max_length=1,
        default='1',
        choices=(
            ('1','Fono 1469'),
            ('2','Patrullaje Preventivo'),
            ('3','Patrullaje colaborativo (carabineros)'),
            ('4','Demanda espontánea'),
            ('5','Fiscalización'),
            ('6','Otro:_____'),
            ),
        verbose_name='Vía de Ingreso',
        )
    via_ingreso_otro = models.CharField(null=True, blank=True, max_length=20, verbose_name=" ")
    denunciante = models.ForeignKey(Denunciante, on_delete=models.PROTECT, verbose_name='denunciante')
    delito = models.ForeignKey(Delito, on_delete=models.PROTECT, verbose_name='Delito')
    delito_otro = models.TextField(null=True, blank=True, verbose_name='Comentario')
    calle = models.CharField(max_length=30, verbose_name="Avenida/Calle/Pasaje")
    numero = models.IntegerField(null=True, blank=True, verbose_name="Numeración")
    complemento_direccion = models.CharField(null=True, blank=True, max_length=50, verbose_name='Complemento de Dirección')
    interseccion = models.CharField(null=True, blank=True, max_length=50, verbose_name='Intersección',)
    prioridad = models.CharField(
        max_length=1,
        default='0',
        choices=(
            ('0','0'),
            ('1','1'),
            ('2','2'),
            ('3','3'),
            ),
        verbose_name='Prioridad',
        )
    resolucion = models.CharField(
        max_length=1,
        default='1',
        choices=(
            ('1','Cursar infracción'),
            ('2','Proceso judicial'),
            ('3','Derivación Área Prevención'),
            ('4','Territorial'),
            ('5','Atención a Víctimas'),
            ('6','Convivencia'),
            ('7','Derivación Unidad especializada'),
            ('8','Intramunicipal ¿cuál?'),
            ('9','Extramunicipal ¿cuál?'),
            ),
        verbose_name='Forma de resolución del requerimiento',
        )
    resolucion_otro = models.CharField(null=True, blank=True, max_length=50, verbose_name='¿Cuál?')
    
    autor = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Autor")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)

    class Meta:
        verbose_name = "Requerimiento"
        verbose_name_plural = "Requerimientos"
        ordering = ['numero_requerimiento']
        
    def save(self, *args, **kwargs):
        if self.numero:
            uv = obtener_uv(self.calle,self.numero)
            self.uv = UV.objects.get(numero_uv=uv)
            return super(Requerimiento, self).save(*args, **kwargs)
        else:
            self.uv = UV.objects.get(numero_uv=0)
            return super(Requerimiento, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.numero_requerimiento} - {self.delito}'