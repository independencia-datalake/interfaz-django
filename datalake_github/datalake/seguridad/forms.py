from django import forms
from django.forms.widgets import (
    RadioSelect,
)
from .models import (
    Requerimiento,
)

class RequerimientoModelForm(forms.ModelForm):
    class Meta:
        model = Requerimiento
        fields = [
            'estatus',
            'identidad',
            'numero_identificacion',
            'nombre',
            'apellido',
            'calle',
            'numero',
            'interseccion',
            'delito_social',
            'violencia_intrafamiliar',
            'incivilidades',
            'abuso_sexual',
            'accidente',
            'comentario',
            'prioridad',
            'resolucion',
            'des_resolucion',
        ]
        widgets = {
            'estatus': RadioSelect(),
            'identidad': RadioSelect(),
            'delito_social': RadioSelect(),
            'violencia_intrafamiliar': RadioSelect(),
            'incivilidades': RadioSelect(),
            'abuso_sexual': RadioSelect(),
            'accidente': RadioSelect(),
            'prioridad': RadioSelect(),
            'resolucion':RadioSelect(),
        }
