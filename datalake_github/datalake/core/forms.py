from django import forms
from django.forms.widgets import (
    RadioSelect,
)

from .models import (
    Persona,
    Telefono,
    Correo,
    Direccion,
)

TIPOS_DE_IDENTIFICACION = [
    ('RUT','Rut'),
    ('PASAPORTE','Pasaporte'),
    ('OTRO','Otro'),
]


class PersonaVerificacionForm(forms.Form):
    tipo_identificacion = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect,
        choices=TIPOS_DE_IDENTIFICACION,
        label='Tipo de identificación',
    )
    numero_identificacion = forms.CharField(max_length=30, label='Número de identificación')                  

    
class PersonaModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonaModelForm,self).__init__(*args, **kwargs)

    class Meta:
        model = Persona
        fields = [
            'tipo_identificacion',
            'numero_identificacion',
            'nombre_persona',
            'apellido_paterno',
            'apellido_materno',
            'fecha_nacimiento',
        ]
        widgets = {
            'tipo_identificacion': RadioSelect(),
            'fecha_nacimiento' : forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }
                ),
        }

class TelefonoModelForm(forms.ModelForm):
    class Meta:
        model = Telefono
        fields = [
            'tipo_telefono',
            'telefono',
        ]
        widgets = {
            'tipo_telefono': RadioSelect(),
        }

class CorreoModelForm(forms.ModelForm):
    class Meta:
        model = Correo
        fields = [
            'tipo_correo',
            'correo',
        ]
        widgets = {
            'tipo_correo': RadioSelect(),
        }

class DireccionModelForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = [
            'calle',
            'numero',
            'complemento_direccion',
        ]
        widgets = {
            'tipo_correo': RadioSelect(),
        }