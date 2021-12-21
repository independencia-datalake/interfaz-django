from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from core.models import (
    obtener_uv,
    Persona,
    UV,
)

class Mascota(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.PROTECT, verbose_name='dueño')
    uv = models.ForeignKey(UV, on_delete=models.PROTECT, verbose_name='Unidad vecinal')
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
    
    def save(self, *args, **kwargs):
        if self.id == None:
            uv = self.persona.uv
            self.uv = uv
            return super(Mascota, self).save(*args, **kwargs)
        else:
            return super(Mascota, self).save(*args, **kwargs)

    def __str__(self):
            return f'{self.nombre}' 

class Procedimiento(models.Model):
    mascota = models.ForeignKey(Mascota,on_delete=models.PROTECT, verbose_name='Mascota')
    uv = models.ForeignKey(UV,on_delete=models.PROTECT, verbose_name='Unidad vecinal')
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
    
    def save(self, *args, **kwargs):
        if self.id == None:
            uv = self.mascota.uv
            self.uv = uv
            return super(Procedimiento, self).save(*args, **kwargs)
        else:
            return super(Procedimiento, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.f_ingreso}'

class ControlPlaga(models.Model):
    persona = models.ForeignKey(Persona,on_delete=models.PROTECT, verbose_name='Persona')
    uv = models.ForeignKey(UV, on_delete=models.PROTECT, verbose_name='Unidad vecinal')
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

    def save(self, *args, **kwargs):
        if self.id == None:
            uv = self.persona.uv
            self.uv = uv
            return super(ControlPlaga, self).save(*args, **kwargs)
        else:
            return super(ControlPlaga, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Control de Plaga"
        verbose_name_plural = "Control de Plagas"
        ordering = ['created']
    
    def __str__(self):
            return f'{self.f_ingreso}' 

    def  get_absolute_url(self):
        return reverse("controldeplaga-inicio")

class SeguridadDIMAP(models.Model):
    persona = models.ForeignKey(Persona,on_delete=models.PROTECT, verbose_name='Denunciante')
    f_ingreso = models.DateField(auto_now_add=True, verbose_name='Fecha de Ingreso')
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
    ficha = models.CharField(max_length=40,default='0',verbose_name='Ficha de Ingreso')
    tipo_denuncia = models.CharField(
        max_length=1,
        choices=(
            ('1','Zoonosis'),
            ('2','Trm'),
            ('3','Higiene Ambiental'),
            ),
        verbose_name='Tipo de Denuncia',
        )
    text_denuncia = models.TextField(blank=True, verbose_name='Motivo Denuncia')
    nombre = models.CharField(null=True, blank=True, max_length=30,verbose_name='Nombre Denunciado')
    apellido = models.CharField(null=True, blank=True, max_length=30,verbose_name='Apellido Denunciado')
    calle = models.CharField(null=True, blank=True, max_length=30, verbose_name='Calle Denunciado')
    numero = models.PositiveIntegerField(null=True, blank=True, verbose_name='Numeración')
    uv = models.ForeignKey(UV, on_delete=models.PROTECT, verbose_name='Unidad Vecinal Demandado')
    telefono = models.CharField(null=True, blank=True, max_length=30, verbose_name='Teléfono Denunciado')
    f_visita = models.DateField(verbose_name='Fecha de visita inspeccion')
    l_transgrsion = models.CharField(
        max_length=1,
        choices=(
            ('1','Vía Pública'),
            ('2','Domicilio'),
            ),
        verbose_name='Lugar de Transgresión',
    )
    i_visita = models.CharField(
        max_length=1,
        choices=(
            ('1','Inspector'),
            ('2','Profesional'),
            ),
        verbose_name='Visita Inspectiva',
    )
    obs_insp = models.TextField(null=True,blank=True,verbose_name='Observación Inspector')
    cat_visita = models.CharField(
        max_length=1,
        default='',
        blank=True,
        choices=(
            ('1','Se Visita, Hay Contacto'),
            ('2','Se Visita, No Hay Contacto'),
            ('3','Otra'),
            ),
        verbose_name='Categorización de Visita',
    )
    notificacion = models.CharField(
        max_length=1,
        default='',
        blank=True,
        choices=(
            ('1','Con Notificación'),
            ('2','Sin Notificación'),
            ),
        verbose_name='Notificación',
    )
    n_notificacion = models.PositiveIntegerField(null=True, blank=True, verbose_name='Número de notificación')
    respuesta = models.TextField(blank=True, verbose_name='Respuesta Denunciante')
    img_respuesta = models.FileField(blank=True, null=True, upload_to='dimap/denuncia/%Y/%m/%d/')

    autor = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Autor")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)

    class Meta:
        verbose_name = "Seguridad DIMAP"
        verbose_name_plural = "Seguridad DIMAP"
        ordering = ['created']

    def save(self, *args, **kwargs):
        if self.calle:
            if self.numero:
                uv = obtener_uv(self.calle,self.numero)
                self.uv = UV.objects.get(numero_uv=uv)
                return super(SeguridadDIMAP, self).save(*args, **kwargs)
            else:
                self.uv = UV.objects.get(numero_uv=0)
                return super(SeguridadDIMAP, self).save(*args, **kwargs)
        else:
            self.uv = UV.objects.get(numero_uv=0)
            return super(SeguridadDIMAP, self).save(*args, **kwargs)
    
    def __str__(self):
            return f'{self.f_ingreso}' 

    def  get_absolute_url(self):
        return reverse("seguridad-inicio")
