from django import forms
from django.db.models import fields
from django.forms.widgets import (
    RadioSelect,
)
from .models import (
    Requerimiento,
    Denunciante,
    ClasificacionDelito,
    Delito,
)

class DenuncianteModelForm(forms.ModelForm):
    class Meta:
        model = Denunciante
        fields = [
            'nombre',
            'apellido',
            'telefono',
            'correo',
        ]

class RequerimientoInicioModelForm(forms.ModelForm):
    class Meta:
        model = Requerimiento
        fields = [
            'estatus',
            'via_ingreso',
            'via_ingreso_otro',
        ]
        widgets = {
            'estatus': RadioSelect(),
            'via_ingreso': RadioSelect(),
        }

class RequerimientoDelitoModelForm(forms.ModelForm):
       
    class Meta:
        model = Requerimiento
        fields = [
            'delito',   #FK
            'delito_otro',
        ]
        widgets = {
            'delito': RadioSelect(),
        }

class RequerimientoUbicacionModelForm(forms.ModelForm):
    class Meta:
        model = Requerimiento
        fields = [
            'calle',
            'numero',
            'complemento_direccion',
            'interseccion',
        ]

class RequerimientoResolucionModelForm(forms.ModelForm):
    class Meta:
        model = Requerimiento
        fields = [
            'prioridad',
            'resolucion',
            'resolucion_otro',
        ]
        widgets = {
            'prioridad': RadioSelect(),
            'resolucion':RadioSelect(),
        }
