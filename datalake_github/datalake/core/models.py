import pandas as pd
from django.db import models

  # FUNCIONES PARA EL CALCULO DE LA UNIDAD VECINAL

def obtener_uv(calle, numero):
  df = pd.read_csv('calculadorauv/static/calculadorauv/streets_uv.csv')
  validaciones = df[df['calle']==calle]
  uv = None

  for index, row in validaciones.iterrows():
    if row['condicion'] == 'PAR':
      uv = validar_par(numero, row)
    elif row['condicion'] == 'IMPAR':
      uv = validar_impar(numero, row)
    elif row['condicion'] == 'NO':
      uv = row['uv']
    elif row['condicion'] == 'MENOR':
      uv = validar_menor(numero,row)
    elif row['condicion'] == 'MAYOR':
      uv = validar_mayor(numero,row)
    elif row['condicion'] == 'ENTRE':
      uv = validar_entre(numero,row)
    elif row['condicion'] == 'PARENTRE':
      uv = validar_parentre(numero,row)
    elif row['condicion'] == 'IMPARENTRE':
      uv = validar_imparentre(numero,row)
    elif row['condicion'] == 'PARMENOR':
      uv = validar_parmenor(numero,row)
    elif row['condicion'] == 'PARMAYOR':
      uv = validar_parmayor(numero,row)  
    elif row['condicion'] == 'IMPARMENOR':
      uv = validar_imparmenor(numero,row)
    elif row['condicion'] == 'IMPARMAYOR':
      uv = validar_imparmayor(numero,row)
    elif row['condicion'] == 'CONJUNTO':
      uv = validar_conjunto(numero,row)
    elif row['condicion'] == 'IGUAL':
      uv = validar_igual(numero,row)    
    if uv != None:
      return uv
  return 0

def validar_par(numero, validacion):
  if numero % 2 == 0:
    return validacion['uv']

def validar_impar(numero, validacion):
  if numero % 2 != 0:
    return validacion['uv']

def validar_menor(numero, validacion):
  if numero < int(validacion['conjunto']):
    return validacion['uv']

def validar_mayor(numero, validacion):
  if numero > int(validacion['conjunto']):
    return validacion['uv']

def validar_entre(numero, validacion):
  lim_inf = int(validacion['conjunto'].split('-')[0])
  lim_sup = int(validacion['conjunto'].split('-')[1])
  if numero > lim_inf and numero < lim_sup:
      return validacion['uv']

def validar_parentre(numero, validacion):
  lim_inf = int(validacion['conjunto'].split('-')[0])
  lim_sup = int(validacion['conjunto'].split('-')[1])
  if numero % 2 == 0 and numero > lim_inf and numero < lim_sup:
      return validacion['uv']

def validar_imparentre(numero, validacion):
  lim_inf = int(validacion['conjunto'].split('-')[0])
  lim_sup = int(validacion['conjunto'].split('-')[1])
  if numero % 2 != 0 and numero > lim_inf and numero < lim_sup:
      return validacion['uv']

def validar_parmenor(numero, validacion):
  if numero % 2 == 0 and numero < int(validacion['conjunto']):
    return validacion['uv']

def validar_parmayor(numero, validacion):
  if numero % 2 == 0 and numero > int(validacion['conjunto']):
    return validacion['uv']

def validar_imparmenor(numero, validacion):
  if numero % 2 != 0 and numero < int(validacion['conjunto']):
    return validacion['uv']

def validar_imparmayor(numero, validacion):
  if numero % 2 != 0 and numero > int(validacion['conjunto']):
    return validacion['uv']

def validar_conjunto(numero, validacion):
  conjunto = validacion['conjunto'].replace('(','')
  conjunto = conjunto.replace(')','')
  conjunto = conjunto.split(' ')
  if str(numero) in conjunto:
    return validacion['uv']

def validar_igual(numero, validacion):
  igual = int(validacion['conjunto'])
  if numero == igual:
    return validacion['uv']


# MODELO CORE

class CallesIndependencia(models.Model):
    calle = models.CharField(max_length=30)

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
    fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento', blank=True, null=True)

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
          ni = self.numero_identificacion
          if ni[-2] == '-':
              return super(Persona, self).save(*args, **kwargs)
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
          return super(Persona, self).save(*args, **kwargs)
        else:
          return super(Persona, self).save(*args, **kwargs)
          
      
      else:
        direcciones = Direccion.objects.filter(persona__exact=self)
        direccion = direcciones.get(active=True)
        uv = direccion.uv
        self.uv = uv

        if self.tipo_identificacion == "RUT":
            ni = self.numero_identificacion
            if ni[-2] == '-':
                return super(Persona, self).save(*args, **kwargs)
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
            return super(Persona, self).save(*args, **kwargs)

        return super(Persona, self).save(*args, **kwargs)
      

    def __str__(self):
        return f'{self.numero_identificacion}'

class Telefono(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name='Persona')
    telefono = models.CharField(null=True, blank=True, max_length=30, verbose_name='Teléfono')
    tipo_telefono = models.CharField(
        null=True,
        blank=False,
        default='MOVIL',
        max_length=30,
        choices=(
            ('MOVIL','Movil'),
            ('CASA','Casa'),
            ('TRABAJO','Trabajo'),
            ('OTRO','Otro'),
            ),
        verbose_name='Tipo de Teléfono'
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
    tipo_correo = models.CharField(
        null=True,
        blank=False,
        default='PERSONAL',
        max_length=30,
        choices=(
            ('PERSONAL','Personal'),
            ('TRABAJO','Trabajo'),
            ('ESCUELA','Escuela'),
            ('OTRO','Otro'),
            ),
        verbose_name='Tipo de Correo'
        )

    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación', editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de edición', editable=False)

    class Meta:
        verbose_name = "Correo Persona"
        verbose_name_plural = "Correos Personas"
        ordering = ['created']

    def __str__(self):
            return f'{self.persona} - {self.tipo_correo} - {self.correo}' 

class Direccion(models.Model):
  active = models.BooleanField(default=True, verbose_name="Activo",null=True)
  persona = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name='Persona')
  uv = models.ForeignKey(UV, on_delete=models.CASCADE, verbose_name='UV')
  calle = models.CharField(max_length=30, verbose_name="Avenida/Calle/Pasaje")
  numero = models.PositiveIntegerField(verbose_name="Numeración")
  complemento_direccion = models.CharField(max_length=50, verbose_name='Complemento de Dirección',blank=True,null=True)

  created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación', editable=False)
  updated = models.DateTimeField(auto_now=True, verbose_name='Fecha de edición', editable=False)

  class Meta:
      verbose_name = "Dirrecion Persona"
      verbose_name_plural = "Direcciones Personas"
      ordering = ['created']

  def save(self, *args, **kwargs):
      print(self.calle)
      print(self.numero)
      uv = obtener_uv(self.calle,self.numero)
      print(uv)
      self.uv = UV.objects.get(numero_uv=uv)
      return super(Direccion, self).save(*args, **kwargs)

  def __str__(self):
          return f'{self.persona} - {self.uv} - {self.calle} {self.numero} - {self.active}' 

