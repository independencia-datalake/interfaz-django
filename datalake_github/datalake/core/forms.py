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

class DateInput(forms.DateInput):
    input_type = 'date'

class PersonaVerificacionForm(forms.Form):
    tipo_identificacion = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect,
        choices=TIPOS_DE_IDENTIFICACION,
    )
    numero_identificacion = forms.CharField(max_length=30)                  

    
class PersonaModelForm(forms.ModelForm):
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
            'fecha_nacimiento' : DateInput(),
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