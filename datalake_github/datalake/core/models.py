from django.db import models

class CallesIndependencia(models.Model):
    calle = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Calle "
        verbose_name_plural = "Calles de Independencia"
        ordering = ['calle']
        
    def __str__(self):
        return f'{self.calle}'

class UV(models.Model):
    numero_uv = models.PositiveIntegerField(verbose_name="Numero de U.V.")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)

    class Meta:
        verbose_name = "Unidad Vecinal"
        verbose_name_plural = "Unidades Vecinales"
        ordering = ['numero_uv']
        
    def __str__(self):
        return f'{self.numero_uv}'

class Persona(models.Model):
    uv = models.ForeignKey(UV, on_delete=models.PROTECT, verbose_name="Unidad Vecinal")
    tipo_identificacion = models.CharField(blank=False, default='RUT', max_length=30,
                                            choices=(
                                                ('RUT','Rut'),
                                                ('PASAPORTE','Pasaporte'),
                                                ('OTRO','Otro'),
                                            ),verbose_name='Tipo de Documento'
                                          ) 
    numero_identificacion = models.CharField(max_length=30, blank=True, verbose_name="Número de Identidad", unique=True)
    nombre_persona = models.CharField(max_length=30, verbose_name="Nombre Persona")
    apellido_paterno = models.CharField(max_length=30, verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(max_length=30, verbose_name="Apellido Materno")
    fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento')
    direccion_persona = models.CharField(max_length=30, verbose_name="Avenida/Calle/Pasaje")
    numero_direccion = models.PositiveIntegerField(verbose_name="Numeración")
    complemento_direccion = models.CharField(max_length=50, verbose_name='Complemento de Dirección',blank=True,null=True)
    telefono_persona = models.CharField(max_length=30, verbose_name="Teléfono")
    correo_persona = models.EmailField(max_length=40, verbose_name="Email")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ['created']

    def save(self, *args, **kwargs):
        if self.tipo_identificacion == "RUT":
            ni = self.numero_identificacion
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
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.numero_identificacion}'

