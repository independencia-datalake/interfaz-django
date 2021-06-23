from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Paises(models.Model): 
    id = models.PositiveIntegerField(primary_key=True, editable=False)
    nombre = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Pais"
        verbose_name_plural = "Paises"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class CallesCondiciones(models.Model):
    calle = models.CharField(max_length=30)
    condiciones = models.TextField()

    class Meta:
        verbose_name = "Calle y UV"
        verbose_name_plural = "Calles y UV"
        ordering = ['calle']
        
    def __str__(self):
        return f'{self.calle}'

class FormularioBase(models.Model):
    nombre_formulario = models.CharField(default="Formulario Base", editable=False, max_length=20)
    p_origen = models.CharField(default="", max_length=30, verbose_name="Pais de Origen")
    tipo_identificacion = models.CharField(default="", max_length=30,
                                            choices=(
                                                ('Rut','Rut'),
                                                ('Pasaporte','Pasaporte'),
                                                ('Otro','Otro'),
                                            )
                                          )
    numero_identificacion = models.CharField(default="", max_length=30)
    nombre = models.CharField(max_length=30, default="", verbose_name='Nombres')
    apellido = models.CharField(max_length=30, default="", verbose_name='Apellidos')
    direccion = models.CharField(default="", max_length=30)
    numero_calle = models.PositiveIntegerField(default=0)
    uv = models.IntegerField(default=0)
    texto1 = models.TextField(blank=True, verbose_name="Texto 1")
    texto2 = models.TextField(blank=True, verbose_name="Texto 2")
    texto3 = models.TextField(blank=True, verbose_name="Texto 3")
    texto4 = models.TextField(blank=True, verbose_name="Texto 4")

    autor = models.ForeignKey(User, on_delete=models.PROTECT)  
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False) 
    
    class Meta:
        verbose_name = "formulario base"
        verbose_name_plural = "formularios bases"
        ordering = ['-created']
  
    def __str__(self):
        return f'{self.created} - {self.numero_identificacion} - {self.nombre_formulario}'
        
    def  get_absolute_url(self):
        return reverse("formulariobase-detail", kwargs={"pk": self.pk})

class Denuncia(models.Model):
    nombre_formulario = models.CharField(default="Denuncias", editable=False, max_length=20)
    estatus = models.CharField(default="Pendiente", max_length=30,
                                            choices=(
                                                ('Pendiente','Pendiente'),
                                                ('Realizado','Realizado'),
                                                ('Anulado','Anulado'),
                                            ),
                                            verbose_name='Estatus'
                                          )    
    tipo_identificacion_denunciante = models.CharField(default="Rut", max_length=30,
                                            choices=(
                                                ('Rut','Rut'),
                                                ('Pasaporte','Pasaporte'),
                                                ('Otro','Otro'),
                                            ),
                                            verbose_name='Tipo de Documento Denunciante'
                                          )
    numero_identificacion_denunciante = models.CharField(default="", blank=True ,max_length=30, verbose_name='Numero de Documento Denunciante')
    nombre_denunciante = models.CharField(max_length=30, default="", verbose_name='Nombres Denunciante')
    apellido_p_denunciante = models.CharField(max_length=30, default="", verbose_name='Apellido Paterno Denunciante')
    apellido_m_denunciante = models.CharField(max_length=30, blank=True,default="", verbose_name='Apellidos Materno Denunciante')
    telefono_denunciante = models.CharField(max_length=30, blank=True,default="", verbose_name='Telefono Denunciante')
    direccion = models.CharField(default="", max_length=30, verbose_name='Calle Denunciante')
    numero_calle = models.PositiveIntegerField(default=0, verbose_name='Numero Calle Denunciante')
    email_denunciante = models.EmailField(max_length=30, blank=True, verbose_name='Email de Contacto Denunciante')
    tipo_denuncia = models.CharField(default="", max_length=30,
                                            choices=(
                                                ('Zoonosis','Zoonosis'),
                                                ('TRM','TRM'),
                                                ('Higene Ambiental','Higene Ambiental'),
                                            ),
                                            verbose_name='Tipo de denuncia'
                                          )
    texto_denuncia = models.TextField(blank=True, verbose_name="Texto de Denuncia")
    nombre_denunciado = models.CharField(blank=True, max_length=30, default="", verbose_name='Nombres Denunciante')
    apellido_p_denunciado = models.CharField(blank=True, max_length=30, default="", verbose_name='Apellido Paterno Denunciado')
    apellido_m_denunciado = models.CharField(blank=True, max_length=30, default="", verbose_name='Apellidos Materno Denunciado')
    telefono_denunciado = models.CharField(blank=True, max_length=30, default="", verbose_name='Telefono Denunciado')
    direccion_denunciado = models.CharField(blank=True, default="", max_length=30, verbose_name='Calle Denunciado')
    numero_calle_denunciado = models.PositiveIntegerField(blank=True, default=0, verbose_name='Numero Calle Denunciado')
    email_denunciado = models.EmailField(blank=True, max_length=30, verbose_name='Email de Contacto Denunciado')
    fecha_visita = models.DateField(auto_now_add=False, auto_now=False, blank=True,verbose_name="Fecha de Visita Inspectiva")
    lugar_de_transgresion =  models.CharField(default="", max_length=30,
                                            choices=(
                                                ('Via Publica','Via Publica'),
                                                ('Domicilio','Domicilio'),
                                            ),
                                            verbose_name='Lugar de Transgrecion'
                                          )
    visita_inspectiva =  models.CharField(default="", max_length=30,
                                            choices=(
                                                ('Inspector','Inspector'),
                                                ('Profesional','Profesional'),
                                            ),
                                            verbose_name='Tipo de Visita Inspectiva'
                                          )
    texto_observacion = models.TextField(blank=True, verbose_name="Texto de Denuncia")
    categoria_visita =  models.CharField(default="", max_length=30,
                                            choices=(
                                                ('Se Visita. Hay Contacto','Se Visita. Hay Contacto'),
                                                ('Se Visita. No Hay Contacto','Se Visita. No Hay Contacto'),
                                                ('Otra','Otra'),
                                            ),
                                            verbose_name='Categoria de Visita Inspectiva'
                                          )
    notificacion =  models.CharField(default="", max_length=30,
                                            choices=(
                                                ('Con Notificacion','Con Notificacion'),
                                                ('Sin Notificacion','Sin Notificacion'),
                                            ),
                                            verbose_name='Notificacion'
                                          )
    numero_noficacion = models.PositiveIntegerField(blank=True, default=0, verbose_name='Numero de Notificacion')
    texto_enviado = models.TextField(blank=True, verbose_name="Texto Respuesta Enviado")
    ver_respuesta = models.ImageField(blank=True, upload_to='verificacion_denuncias')

    uv = models.IntegerField(default=0)
    uv_denunciado = models.IntegerField(blank=True, default=0)
    autor = models.ForeignKey(User, on_delete=models.PROTECT)  
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición") 
    
    class Meta:
        verbose_name = "Denuncia"
        verbose_name_plural = "Denuncias"
        ordering = ['-created']
  
    def __str__(self):
        return f'{self.created} - {self.numero_identificacion_denunciante} - {self.nombre_formulario}'
        
    def  get_absolute_url(self):
        return reverse("denuncia-detail", kwargs={"pk": self.pk})    

class ControlDePlaga(models.Model):
    nombre_formulario = models.CharField(default="Control de Plagas", editable=False, max_length=20)
    estatus = models.CharField(default="Pendiente", max_length=30,
                                            choices=(
                                                ('Pendiente','Pendiente'),
                                                ('Realizado','Realizado'),
                                                ('Anulado','Anulado'),
                                            ), 
                                            verbose_name='Estatus'
                                            )    
    ficha_numero = models.PositiveIntegerField(blank=True, default=0, verbose_name='Numero de Ficha')
    tipo_identificacion = models.CharField(default="Rut", max_length=30,
                                            choices=(
                                                ('Rut','Rut'),
                                                ('Pasaporte','Pasaporte'),
                                                ('Otro','Otro'),
                                            ),
                                            verbose_name='Tipo de Documento'
                                            )
    numero_identificacion = models.CharField(default="", blank=True ,max_length=30, verbose_name='Numero de Documento')
    nombre = models.CharField(max_length=30, default="", verbose_name='Nombres')
    apellido_p = models.CharField(max_length=30, default="", verbose_name='Apellido Paterno')
    apellido_m = models.CharField(max_length=30, blank=True,default="", verbose_name='Apellidos Materno')
    telefono = models.CharField(max_length=30, blank=True,default="", verbose_name='Telefono')
    direccion = models.CharField(default="", max_length=30, verbose_name='Calle')
    numero_calle = models.PositiveIntegerField(default=0, verbose_name='Numero Calle')
    email = models.EmailField(max_length=30, blank=True, verbose_name='Email de Contacto')
    tipo_solicitud = models.CharField(default="", max_length=30,
                                            choices=(
                                                ('Desratizar','Desratizar'),
                                                ('Fumigar','Fumigar'),
                                                ('Sanitizar','Sanitizar'),
                                            ),
                                            verbose_name='Tipo de Solicitud'
                                          )
    fecha_coordinada = models.DateField(auto_now_add=False, auto_now=False, blank=True,verbose_name="Fecha Coordinada", null=True)
    jornada =  models.CharField(default="", max_length=30,
                                            choices=(
                                                ('Mañana','Mañana'),
                                                ('Tarde','Tarde'),
                                            ),
                                            verbose_name='Jornada de Servicio'
                                          )
    fecha_visita = models.DateField(auto_now_add=False, auto_now=False, blank=True,verbose_name="Fecha Operacion", null=True)
    producto =  models.CharField(default="", max_length=30,
                                            choices=(
                                                ('RATAMIX','RATAMIX'),
                                                ('DELTA MAX','DELTA MAX'),
                                                ('DUPLALIM','DUPLALIM'),
                                            ),
                                            verbose_name='Producto Utilizado'
                                          )

    uv = models.IntegerField(default=0)
    autor = models.ForeignKey(User, on_delete=models.PROTECT)  
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición") 
    
    class Meta:
        verbose_name = "Control de Plaga"
        verbose_name_plural = "Controles de Plagas"
        ordering = ['-created']
  
    def __str__(self):
        return f'{self.created} - {self.numero_identificacion} - {self.nombre_formulario}'
        
    def  get_absolute_url(self):
        return reverse("controldeplaga-detail", kwargs={"pk": self.pk})    

class Esterilizacion(models.Model):
    nombre_formulario = models.CharField(default="Esterilizacion", editable=False, max_length=20)
    estatus = models.CharField(default="Pendiente", max_length=30,
                                            choices=(
                                                ('Pendiente','Pendiente'),
                                                ('Realizado','Realizado'),
                                                ('Anulado','Anulado'),
                                            ),
                                            verbose_name='Estatus'
                                          )    
    tipo_identificacion = models.CharField(default="Rut", max_length=30,
                                            choices=(
                                                ('Rut','Rut'),
                                                ('Pasaporte','Pasaporte'),
                                                ('Otro','Otro'),
                                            ),
                                            verbose_name='Tipo de Documento'
                                          )
    numero_identificacion = models.CharField(default="", blank=True ,max_length=30, verbose_name='Numero de Documento')
    nombre = models.CharField(max_length=30, default="", verbose_name='Nombres')
    apellido_p = models.CharField(max_length=30, default="", verbose_name='Apellido Paterno')
    apellido_m = models.CharField(max_length=30, blank=True,default="", verbose_name='Apellidos Materno')
    telefono = models.CharField(max_length=30, blank=True,default="", verbose_name='Telefono')
    direccion = models.CharField(default="", max_length=30, verbose_name='Calle')
    numero_calle = models.PositiveIntegerField(default=0, verbose_name='Numero Calle')
    email = models.EmailField(max_length=30, blank=True, verbose_name='Email de Contacto')
    mascota = models.CharField(default="", max_length=30,
                                            choices=(
                                                ('Canino','Canino'),
                                                ('Felino','Felino'),
                                            ),
                                            verbose_name='Especie Mascota'
                                          )
    nombre_mascota = models.CharField(max_length=30, default="", verbose_name='Nombre Mascota')
    sexo_mascota = models.CharField(default="", max_length=30,
                                            choices=(
                                                ('Masculino','Masculino'),
                                                ('Femenino','Femenino'),
                                            ),
                                            verbose_name='Sexo de Mascota'
                                          )
    fecha_cirugia = models.DateField(auto_now_add=False, auto_now=False, blank=True,verbose_name="Fecha Coordinada")
    clinica =  models.CharField(default="", max_length=30,
                                            choices=(
                                                ('Municipal (movil)','Municipal (movil)'),
                                                ('Particular','Particular'),
                                            ),
                                            verbose_name='Tipo de Clinica'
                                          )
    asistencia =  models.CharField(default="", max_length=30,
                                            choices=(
                                                ('Asiste','Asiste'),
                                                ('No Asiste','No Asiste'),
                                                ('Pendiente de Hora','Pendiente de Hora'),
                                            ),
                                            verbose_name='Producto Utilizado'
                                          )
    rechazo = models.TextField(blank=True, verbose_name="Motivo Rechazo")

    uv = models.IntegerField(default=0)
    autor = models.ForeignKey(User, on_delete=models.PROTECT)  
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición") 
    
    class Meta:
        verbose_name = "Esterilizacion"
        verbose_name_plural = "Esterilizaciones"
        ordering = ['-created']
  
    def __str__(self):
        return f'{self.created} - {self.numero_identificacion} - {self.nombre_formulario}'
        
    def  get_absolute_url(self):
        return reverse("esterilizacion-detail", kwargs={"pk": self.pk}) 


