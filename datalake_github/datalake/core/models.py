from ayuda_funciones.rut import calculadora_rut
from ayuda_funciones.uv import obtener_uv
from django.db import models

  # FUNCIONES PARA EL CALCULO DE LA UNIDAD VECINAL

# MODELO CORE

class CallesIndependencia(models.Model):
    calle = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Calle "
        verbose_name_plural = "Calles de Independencia"
        ordering = ['calle']
        
    def __str__(self):
        return f'{self.calle}'

class UV(models.Model):
    numero_uv = models.PositiveIntegerField(verbose_name="Número de U.V.")

    class Meta:
        verbose_name = "Unidad Vecinal"
        verbose_name_plural = "Unidades Vecinales"
        ordering = ['numero_uv']
        
    def __str__(self):
        return f'{self.numero_uv}'

class Persona(models.Model):
    uv = models.ForeignKey(UV, on_delete=models.PROTECT, verbose_name="Unidad Vecinal")
    tipo_identificacion = models.CharField(blank=False, default='RUT', max_length=200,
                                            choices=(
                                                ('RUT','Rut'),
                                                ('PASAPORTE','Pasaporte'),
                                                ('OTRO','Otro'),
                                            ),verbose_name='Tipo de Documento'
                                          ) 
    numero_identificacion = models.CharField(max_length=200, blank=True, verbose_name="Número de Identidad", unique=True)

    nombre_persona = models.CharField(max_length=200, verbose_name="Nombre Persona")
    apellido_paterno = models.CharField(max_length=200, verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(max_length=200, verbose_name="Apellido Materno")
    fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento', blank=True, null=True)
    estado_civil = models.CharField(
        null=True,
        blank=True,
        default='MOVIL',
        max_length=200,
        choices=(
            ('SOLTEO/A','Soltero/a'),
            ('CASADO/A','Casado/a'),
            ('VIUDO/A','Viudo/a'),
            ('UNION CIVIL','Union Civil'),
            ('DIVORSIADO/A','Divorsiado/a')
            ),
        verbose_name='Estado Civil'
        )
    hijos = models.PositiveIntegerField(default=0, verbose_name="Hijos",null=True, blank=True)
    nacionalidad = models.CharField(max_length=200, verbose_name="Nacionalidad",null=True, blank=True)
    enfermedad = models.CharField(max_length=200, verbose_name="Enfermedad",null=True, blank=True)
    medicamento = models.CharField(max_length=200, verbose_name="Medicamento",null=True, blank=True)
    lugar_de_atencion = models.CharField(max_length=200, verbose_name="lLugar De Atencion",null=True, blank=True)
    discapacidad = models.BooleanField(default = False, verbose_name = "Discapacidad",null=True, blank=True)
    certificado_compin = models.BooleanField(default = False, verbose_name = "Certificado Compin",null=True, blank=True)
    embarazo = models.BooleanField(default = False, verbose_name = "Embarazo",null=True, blank=True)
    certificado_embarazo = models.BooleanField(default = False, verbose_name = "Certificado Embarazo",null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)

    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ['created']

    def save(self, *args, **kwargs):
      if self.id == None:
        self.uv = UV.objects.get(numero_uv=0)
        if self.tipo_identificacion == "RUT":
          self.numero_identificacion = calculadora_rut(self.numero_identificacion)
      
        return super(Persona, self).save(*args, **kwargs)

      else:
        direcciones = Direccion.objects.filter(persona__exact=self)
        direccion = direcciones.get(active=True)
        uv = direccion.uv
        self.uv = uv

        if self.tipo_identificacion == "RUT":
          self.numero_identificacion = calculadora_rut(self.numero_identificacion)

        return super(Persona, self).save(*args, **kwargs)
      
    def __str__(self):
        return f'{self.numero_identificacion}'

class Telefono(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name='Persona')
    telefono = models.CharField(null=True, blank=True, max_length=200, verbose_name='Teléfono')
    telefono_secundario = models.CharField(null=True, blank=True, max_length=200, verbose_name='Teléfono Secundario')
    tipo_telefono = models.CharField(
        null=True,
        blank=False,
        default='MOVIL',
        max_length=200,
        choices=(
            ('MOVIL','Movil'),
            ('CASA','Casa'),
            ('TRABAJO','Trabajo'),
            ('OTRO','Otro'),
            ),
        verbose_name='Tipo de Teléfono'
        )
    tipo_telefono_secundario = models.CharField(
      null=True,
      blank=False,
      default='NO APLICA',
      max_length=200,
      choices=(
          ('MOVIL','Movil'),
          ('CASA','Casa'),
          ('TRABAJO','Trabajo'),
          ('OTRO','Otro'),
          ('NO APLICA', 'No Aplica'),
          ),
      verbose_name='Tipo de Teléfono Secundario'
      )

    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación', editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de edición', editable=False)

    class Meta:
        verbose_name = "Teléfono Persona"
        verbose_name_plural = "Teléfonos Personas"
        ordering = ['created']
    
    def __str__(self):
            return f'{self.persona} - {self.tipo_telefono} - {self.telefono}' 

class Correo(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name='Persona')
    correo = models.EmailField(max_length=40, verbose_name="Email")
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación', editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de edición', editable=False)

    class Meta:
        verbose_name = "Correo Persona"
        verbose_name_plural = "Correos Personas"
        ordering = ['created']

    def __str__(self):
            return f'{self.persona} - {self.correo}' 

class Direccion(models.Model):
  active = models.BooleanField(default=True, verbose_name="Activo",null=True)
  persona = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name='Persona')
  uv = models.ForeignKey(UV, on_delete=models.CASCADE, verbose_name='UV')
  calle = models.CharField(max_length=200, verbose_name="Avenida/Calle/Pasaje")
  numero = models.PositiveIntegerField(verbose_name="Numeración")
  complemento_direccion = models.CharField(max_length=50, verbose_name='Complemento de Dirección',blank=True,null=True)

  created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación', editable=False)
  updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de edición', editable=False)

  class Meta:
      verbose_name = "Dirrecion Persona"
      verbose_name_plural = "Direcciones Personas"
      ordering = ['created']

  def save(self, *args, **kwargs):
      uv = obtener_uv(self.calle,self.numero)
      self.uv = UV.objects.get(numero_uv=uv)
      return super(Direccion, self).save(*args, **kwargs)

  def __str__(self):
          return f'{self.persona} - {self.uv} - {self.calle} {self.numero} - {self.active}' 

class PersonaInfoSalud(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name='Persona')
    prevision = models.CharField(
        max_length=30, 
        default= 'NINGUNA',
        choices=(
            ('FONASA','Fonasa'),
            ('DIPRECA-CAPREDENA','Dipreca-Capredena'),
            ('ISAPRE','Isapre'),
            ('NINGUNA','Ninguna'),
            ),
        verbose_name="Prevision de Salud")
    isapre = models.CharField(default="NO APLICA" ,max_length=30, null=True,blank=False,
        choices=(
            ('NO APLICA', 'No Aplica'),
            ('BANMEDICA','Banmedica'),
            ('ISALUD','Isalud'),
            ('COLMENA','Colmena'),
            ('CONSALUD','Consalud'),
            ('CRUZBLANCA','Cruz Blanca'),
            ('CRUZ DEL NORTE','Cruz del Norte'),
            ('NUEVA MASVIDA', 'Nueva Masvida'),
            ('FUNDACION','Fundacion'),
            ('VIDA TRES','Vida Tres'),
            ('ESENCIAL','Esencial'),
            ),
            verbose_name="Isapre")
    comentarios = models.CharField(max_length=200, verbose_name="Comentarios ", null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación', editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de edición', editable=False)

    class Meta:
      verbose_name = 'Informacion de salud Persona'
      verbose_name_plural = 'Informacion de salud Personas'
      ordering = ['created']


    def save(self, *args, **kwargs):
        prevision = self.prevision
        if prevision != 'ISAPRE':
          self.isapre = 'NO APLICA'
        return super(PersonaInfoSalud, self).save(*args, **kwargs)


    def __str__(self):
      return f'{self.persona}'

    def save(self, *args, **kwargs):
      if self.prevision != 'ISAPRE':
        self.isapre = 'NO APLICA'
        return super(PersonaInfoSalud, self).save(*args, **kwargs)
      else:
        return super(PersonaInfoSalud, self).save(*args, **kwargs)
      
