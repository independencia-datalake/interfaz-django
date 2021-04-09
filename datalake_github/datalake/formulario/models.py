from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Paises(models.Model): 
    id = models.PositiveIntegerField(primary_key=True, editable=False)
    nombre = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Pais"
        verbose_name_plural = "Paises"
        ordering = ['-nombre']

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

class FormularioOMIL(models.Model):
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
    
    nombre_formulario = models.CharField(default="Formulario OMIL", editable=False, max_length=20)

    class Meta:
        verbose_name = "formulario base"
        verbose_name_plural = "formularios bases"
        ordering = ['-created']
  
    def __str__(self):
        return f'{self.created} - {self.numero_identificacion} - {self.nombre_formulario}'
        
    def  get_absolute_url(self):
        return reverse("formularioomil-detail", kwargs={"pk": self.pk})
    
class Seguridad(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    nombre = models.CharField(max_length=30, default="", verbose_name='Nombres')
    apellido = models.CharField(max_length=30, default="", verbose_name='Apellidos')
    c_telefono = models.PositiveIntegerField(default="569", verbose_name='Codigo de Telefono', blank=True)
    n_telefono = models.CharField(max_length=30, default="11111111", verbose_name="Numero de Telefono", blank=True)
    direccion = models.CharField(default="", max_length=30, verbose_name="Nombre de Calle", blank=True)
    numero_calle = models.PositiveIntegerField(default=0, verbose_name="Numero de Casa", blank=True)
    complemento_direccion = models.TextField(blank=True, verbose_name="Complemento Direccion")
    res_denuncia = models.TextField(blank=True, verbose_name="Resumen de la Denuncia")
    tipi_reclamo = models.CharField(max_length=30, verbose_name="Tipificacion Reclamo", blank=True)
    tipi_denuncia = models.TextField(blank=True, verbose_name="Tipificacion Denuncias")
    cuadrante = models.PositiveIntegerField(verbose_name="Cuadrante", blank=True)
    n_movil = models.CharField(max_length=30, verbose_name="Numero de Movil", blank=True)
    emergencias = models.TextField(blank=True, verbose_name="Emergencias")
    derv_emergencias = models.CharField(max_length=30, verbose_name="Derivaciones de Emergencias", blank=True)
    des_caso = models.TextField(blank=True, verbose_name="Descripcion Caso")
    iden_carab = models.CharField(max_length=30, verbose_name="Identificacion Carabineros", blank=True)
    iden_aav = models.CharField(max_length=30, verbose_name="Identificacion AAV", blank=True)
    departamento = models.CharField(max_length=30, verbose_name="Departamento", blank=True)
    inf_general = models.TextField(blank=True, verbose_name="Informacion General")
    
    nombre_formulario = models.CharField(default="Formulario Seguridad", editable=False, max_length=20)    
    uv = models.IntegerField(default=0, verbose_name="Unidad Vecinal")
    autor = models.ForeignKey(User, on_delete=models.PROTECT)  
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False) 

    class Meta:
        verbose_name = "formulario seguridad"
        verbose_name_plural = "formularios de seguridad"
        ordering = ['-created']
  
    def __str__(self):
        return f'{self.nombre_formulario} - {self.created}'
        
    def  get_absolute_url(self):
        return reverse("seguridad-detail", kwargs={"pk": self.pk})

class Farmacia(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
    numero_identificacion = models.CharField(default="", max_length=30)
    tipo_identificacion = models.CharField(default="", max_length=30,
                                            choices=(
                                                ('RUT','RUT'),
                                                ('PASAPORTE','PASAPORTE'),
                                                ('OTRO','OTRO'),
                                            )
                                          )
    nombre = models.CharField(max_length=30, default="", verbose_name='Nombres')
    apellido = models.CharField(max_length=30, default="", verbose_name='Apellidos')
    direccion = models.CharField(default="", max_length=30, verbose_name="Nombre de Calle", blank=True)
    numero_calle = models.PositiveIntegerField(default=0, verbose_name="Numero de Casa", blank=True)
    n_ficha = models.PositiveIntegerField(default=0, verbose_name="Numero de Ficha", blank=True)
    complemento_direccion = models.TextField(blank=True, verbose_name="Complemento Direccion")
    c_telefono = models.PositiveIntegerField(default="569", verbose_name='Codigo de Telefono', blank=True)
    n_telefono = models.CharField(max_length=30, default="11111111", verbose_name="Numero de Telefono", blank=True)
    fecha_nacimiento = models.CharField(max_length=10, verbose_name="Fecha de Nacimiento", blank=True)
    sis_salud = models.CharField(default="", max_length=30,
                                            choices=(
                                                ('FONASA','FONASA'),
                                                ('ISAPRE','ISAPRE'),
                                                ('NINGUNO','NINGUNO'),
                                                ('OTRO','OTRO'),
                                            )
                                          )
    estado_civil = models.CharField(default="", max_length=30,
                                            choices=(
                                                ('SOLTERA/O','SOLTERA/O'),
                                                ('CASADA/O','CASADA/O'),
                                                ('CONVIVIENTE CIVIL','CONVIVIENTE CIVIL'),
                                                ('VIUDA/O','VIUDA/O'),
                                                ('DIVORCIADA/O','DIVORCIADA/O'),
                                            )
                                          )
    numero_hijos = models.PositiveIntegerField(default=0, verbose_name="Numero de Hijos", blank=True)
    p_origen = models.CharField(default="", max_length=30, verbose_name="Pais de Origen")
    email_form = models.EmailField(max_length=30, blank=True, verbose_name="Direccion de Email")
    enfermedad = models.CharField(default="", max_length=30, verbose_name="Enfermedad")
    med_uso_per = models.CharField(default="", max_length=30, verbose_name="Medicamentos de Uso Permanente")
    lugar_atencion = models.CharField(default="", max_length=30,
                                            choices=(
                                                ('CESFAM CRUZ MELO','CESFAM CRUZ MELO'),
                                                ('CESFAM JUAN ANTONIO RÍOS','CESFAM JUAN ANTONIO RÍOS'),
                                            )
                                          )
    discapacidad = models.BooleanField(blank=True, verbose_name="Posee Discapacidad")
    discapacidad_doc = models.FileField(upload_to='farmacia/discapacidad/%Y/%m/', verbose_name="Documento de Discapacidad", blank=True)
    embarazo = models.BooleanField(blank=True, verbose_name="Esta Embarazada")
    embarazo_doc = models.FileField(upload_to='farmacia/embarazo/%Y/%m/', verbose_name="Documento de Embarazo", blank=True)

    nombre_formulario = models.CharField(default="Formulario Farmacia", editable=False, max_length=20)    
    uv = models.IntegerField(default=0, verbose_name="Unidad Vecinal")
    autor = models.ForeignKey(User, on_delete=models.PROTECT)  
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False) 

    class Meta:
        verbose_name = "formulario farmacia"
        verbose_name_plural = "formularios de farmacias"
        ordering = ['-created']
  
    def __str__(self):
        return f'{self.nombre_formulario} - {self.created} - {self.numero_identificacion}'
        
    def  get_absolute_url(self):
        return reverse("farmacia-detail", kwargs={"pk": self.pk})