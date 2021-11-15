from django import forms
from django.forms.widgets import (
    RadioSelect,
)
from core.forms import (
    DateInput,
)
from .models import (
    Mascota,
    Procedimiento,
    ControlPlaga,
    SeguridadDIMAP,
)


class MascotaModelForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = [
            'nombre',
            'sexo',
            'especie',
        ]
        widgets = {
            'sexo': RadioSelect(),
            'especie': RadioSelect(),
        }

class ProcedimientoModelForm(forms.ModelForm):
    class Meta:
        model = Procedimiento
        fields = [
            'estatus',
            'f_cirugia',
            'clinica',
            'asistencia',
            'ejecucion_cirugia',
            'motivo_rechazo',
        ]
        widgets = {
            'estatus': RadioSelect(),
            'clinica': RadioSelect(),
            'asistencia': RadioSelect(),
            'ejecucion_cirugia': RadioSelect(),
            'f_cirugia' : DateInput(),
        }


class ControlPlagaModelForm(forms.ModelForm):
    class Meta:
        model = ControlPlaga
        fields = [
            'estatus',
            'ficha',
            'tipo_control',
            'f_coordinacion',
            'jornada_servicio',
            'f_operacion',
            'producto',
        ]
        widgets = {
            'estatus': RadioSelect(),
            'tipo_control': RadioSelect(),
            'jornada_servicio':RadioSelect(),
            'producto': RadioSelect(),
            'f_coordinacion' : DateInput(),
            'f_operacion': DateInput(),
        }

class SeguridadDIMAPModelForm(forms.ModelForm):
    class Meta:
        model = SeguridadDIMAP
        fields = [
            'estatus',
            'ficha',
            'tipo_denuncia',
            'text_denuncia',
            'nombre',
            'apellido',
            'calle',
            'numero',
            'telefono',
            'f_visita',
            'l_transgrsion',
            'i_visita',
            'obs_insp',
            'cat_visita',
            'notificacion',
            'n_notificacion',
            'respuesta',
            'img_respuesta',
        ]
        widgets = {
            'estatus': RadioSelect(),
            'tipo_denuncia': RadioSelect(),
            'l_transgrsion': RadioSelect(),
            'i_visita': RadioSelect(),
            'cat_visita': RadioSelect(),
            'notificacion': RadioSelect(),
            'f_visita' : DateInput(),
        }