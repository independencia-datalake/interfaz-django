from django import forms
from django.forms.widgets import (
    RadioSelect,
)
from core.forms import (
    DateInput,
)
from .models import (
    Esterilizacion,
)

# estatus = models.CharField(
#     max_length=1,
#     default='1',
#     choices=(
#         ('1','Pendiente'),
#         ('2','Realizado'),
#         ('3','Anulado'),
#         ),
#     verbose_name='Estatus',
#     )
# f_ingreso = models.DateField(auto_now_add=True, verbose_name='Fecha de Ingreso')
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
# f_cirugia = models.DateField(blank=True, verbose_name='Fecha de Cirugia')
# clinica = models.CharField(
#     max_length=1,
#     default='1',
#     choices=(
#         ('1','Municipalidad (movil)'),
#         ('2','Particular'),
#         ),
#     verbose_name='Clinica',
#     )
# asistencia = models.CharField(
#     max_length=1,
#     default='3',
#     choices=(
#         ('1','Asiste'),
#         ('2','No Asiste'),
#         ('3','Pendiente de Hora'),
#         ),
#     verbose_name='Asistencia',
#     )
# ejecucion_cirugia = models.CharField(
#     max_length=1,
#     default='1',
#     choices=(
#         ('1','Realizada'),
#         ('2','Rechazada'),
#         ),
#     verbose_name='Ejecución Cirugía',
#     )
# motivo_rechazo = models.TextField(blank=True, verbose_name='Motivo Rechazo')


class EsterilizacionModelForm(forms.ModelForm):
    class Meta:
        model = Esterilizacion
        fields = [
            'estatus',
            'i_resp',
            'numero_identificacion',
            'nombre_responsable',
            'apellido_responsable',
            'telefono_responsable',
            'direccion_responsable',
            'numero_direccion',
            'correo_responsable',
            'especie',
            'nombre_mascota',
            'sexo_mascota',
            'f_cirugia',
            'clinica',
            'asistencia',
            'ejecucion_cirugia',
            'motivo_rechazo',
        ]
        widgets = {
            'estatus': RadioSelect(),
            'i_resp': RadioSelect(),
            'especie': RadioSelect(),
            'sexo_mascota': RadioSelect(),
            'clinica': RadioSelect(),
            'asistencia': RadioSelect(),
            'ejecucion_cirugia': RadioSelect(),
            'f_cirugia' : DateInput(),
        }