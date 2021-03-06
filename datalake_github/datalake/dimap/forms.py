from django import forms
from django.forms.widgets import (
    RadioSelect,
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
            'f_cirugia' : forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }
                ),
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
            'f_coordinacion' : forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }
                ),
            'f_operacion': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }
                ),
        }


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
            'f_coordinacion': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }
                ),
            'f_operacion': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }
                ),
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
            'f_visita' : forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }
                ),
        }
