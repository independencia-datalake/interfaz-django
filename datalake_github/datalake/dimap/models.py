from django.contrib.auth.models import User
from django.db import models
from core.models import (
    UV
)

class Esterilizacion(models.Model):
    estatus = models.CharField(
        max_length=1,
        default='1',
        choices=(
            ('1','Pendiente'),
            ('2','Realizado'),
            ('3','Anulado'),
            ),
        verbose_name='Estatus',
        )
    f_ingreso = models.DateField(auto_now_add=True, verbose_name='Fecha de Ingreso')
    i_resp = models.CharField(
        max_length=1,
        default='3',
        choices=(
            ('1','Rut'),
            ('2','Pasaporte'),
            ('3','Otro'),
            ),
        verbose_name='Identificacion Responsable',
        )
    numero_identificacion = models.CharField(max_length=30, blank=True, verbose_name="Número de Identidad Resposnsable")
    nombre_responsable = models.CharField(max_length=30, verbose_name="Nombre Responsable")
    apellido_responsable = models.CharField(max_length=30, verbose_name="Apellido Responsable")
    telefono_responsable = models.CharField(max_length=30, verbose_name="Teléfono Responsable")
    direccion_responsable = models.CharField(max_length=30, verbose_name="Avenida/Calle/Pasaje")
    numero_direccion = models.PositiveIntegerField(verbose_name="Numeración")
    correo_responsable = models.EmailField(null=True, blank=True, max_length=40, verbose_name="Email")
    especie = models.CharField(
        max_length=1,
        default='1',
        choices=(
            ('1','Canino'),
            ('2','Felino'),
            ),
        verbose_name='Especie de Mascota',
        )
    nombre_mascota = models.CharField(max_length=30, verbose_name="Nombre de Mascota")
    sexo_mascota = models.CharField(
        max_length=1,
        default='1',
        choices=(
            ('1','Hembra'),
            ('2','Macho'),
            ),
        verbose_name='Sexo de Mascota',
        )
    f_cirugia = models.DateField(blank=True, verbose_name='Fecha de Cirugia')
    clinica = models.CharField(
        max_length=1,
        default='1',
        choices=(
            ('1','Municipalidad (movil)'),
            ('2','Particular'),
            ),
        verbose_name='Clinica',
        )
    asistencia = models.CharField(
        max_length=1,
        default='3',
        choices=(
            ('1','Asiste'),
            ('2','No Asiste'),
            ('3','Pendiente de Hora'),
            ),
        verbose_name='Asistencia',
        )
    ejecucion_cirugia = models.CharField(
        max_length=1,
        default='1',
        choices=(
            ('1','Realizada'),
            ('2','Rechazada'),
            ),
        verbose_name='Ejecución Cirugía',
        )
    motivo_rechazo = models.TextField(blank=True, verbose_name='Motivo Rechazo')

    uv = models.ForeignKey(UV, on_delete=models.PROTECT, verbose_name="Unidad Vecinal")
    autor = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Autor")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)

    def save(self, *args, **kwargs):
        if self.i_resp == "1":
            ni = self.numero_identificacion
            if ni[-2] == '-':
                return super(Esterilizacion, self).save(*args, **kwargs)
            else:
                if len(ni)==0:
                    None
                elif len(ni)>10:
                    rut = ni[:-10]+'.'+ni[-10:-7]+'.'+ni[-7:-4]+'.'+ni[-4:-1]+'-'+ni[-1]
                    self.numero_identificacion = rut  
                elif len(ni)==9:
                    rut = ni[-10:-7]+'.'+ni[-7:-4]+'.'+ni[-4:-1]+'-'+ni[-1]
                    self.numero_identificacion = rut  
                else:
                    rut = ni[-9:-7]+'.'+ni[-7:-4]+'.'+ni[-4:-1]+'-'+ni[-1]
                    self.numero_identificacion = rut  
        return super(Esterilizacion, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.estatus} - {self.numero_identificacion}'