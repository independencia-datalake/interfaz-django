from django.contrib.auth.models import User
from django.db import models
from django.db.models.base import Model
from core.models import (
    Persona,
)

class Mascota(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT, verbose_name='dueño')
    nombre = models.CharField(max_length=30, verbose_name="Nombre Mascota")
    sexo = models.CharField(
        max_length=1,
        default='1',
        choices=(
            ('1','Hembra'),
            ('2','Macho'),
            ),
        verbose_name='Sexo de Mascota',
        )
    especie = models.CharField(
        max_length=1,
        default='1',
        choices=(
            ('1','Canino'),
            ('2','Felino'),
            ),
        verbose_name='Especie de Mascota',
        )
    
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)

    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"
        ordering = ['nombre']
    
    def __str__(self):
            return f'{self.nombre}' 

class Procedimiento(models.Model):
    mascota = models.ForeignKey(Mascota,on_delete=models.PROTECT, verbose_name='Mascota')
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
    f_cirugia = models.DateField(verbose_name='Fecha de Cirugia')
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
        default='',
        choices=(
            ('1','Realizada'),
            ('2','Rechazada'),
            ),
        verbose_name='Ejecución Cirugía',
        blank=True,
        )
    motivo_rechazo = models.TextField(blank=True, verbose_name='Motivo Rechazo')

    autor = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Autor")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)
    
    # i_resp = models.CharField(
    #     max_length=1,
    #     default='3',
    #     choices=(
    #         ('1','Rut'),
    #         ('2','Pasaporte'),
    #         ('3','Otro'),
    #         ),
    #     verbose_name='Identificacion Responsable',
    #     )
    # numero_identificacion = models.CharField(max_length=30, blank=True, verbose_name="Número de Identidad Resposnsable")
    # nombre_responsable = models.CharField(max_length=30, verbose_name="Nombre Responsable")
    # apellido_responsable = models.CharField(max_length=30, verbose_name="Apellido Responsable")
    # telefono_responsable = models.CharField(max_length=30, verbose_name="Teléfono Responsable")
    # direccion_responsable = models.CharField(max_length=30, verbose_name="Avenida/Calle/Pasaje")
    # numero_direccion = models.PositiveIntegerField(verbose_name="Numeración")
    # correo_responsable = models.EmailField(null=True, blank=True, max_length=40, verbose_name="Email") 
    # especie = models.CharField(
    #     max_length=1,
    #     default='1',
    #     choices=(
    #         ('1','Canino'),
    #         ('2','Felino'),
    #         ),
    #     verbose_name='Especie de Mascota',
    #     )
    # nombre_mascota = models.CharField(max_length=30, verbose_name="Nombre de Mascota")
    # sexo_mascota = models.CharField(
    #     max_length=1,
    #     default='1',
    #     choices=(
    #         ('1','Hembra'),
    #         ('2','Macho'),
    #         ),
    #     verbose_name='Sexo de Mascota',
    #     )

    def __str__(self):
        return f'{self.f_ingreso}'

class ControlPlaga(models.Model):
    persona = models.ForeignKey(Persona,on_delete=models.PROTECT, verbose_name='Persona')
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
    ficha = models.CharField(max_length=40,default='0',verbose_name='Folio ingreso')
    tipo_control = models.CharField(
        max_length=1,
        choices=(
            ('1','Desratizar'),
            ('2','Fumigar'),
            ('3','Sanitizar'),
            ),
        verbose_name='Tipo de Control',
        )
    f_coordinacion = models.DateField(verbose_name='Fecha de Coordinacion')
    jornada_servicio = models.CharField(
        max_length=1,
        choices=(
            ('1','Mañana'),
            ('2','Tarde'),
            ),
        verbose_name='Jornada',
        )
    f_operacion = models.DateField(null=True,blank=True, verbose_name='Fecha de Operacion')
    producto = models.CharField(
        null=True,
        blank=True,
        max_length=1,
        choices=(
            ('1','Ratamix'),
            ('2','Delta Max'),
            ('3','Duplalim'),
            ),
        verbose_name='Producto',
        )

    autor = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Autor")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)

    class Meta:
        verbose_name = "Control de Plaga"
        verbose_name_plural = "Control de Plagas"
        ordering = ['created']
    
    def __str__(self):
            return f'{self.f_ingreso}' 