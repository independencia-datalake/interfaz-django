from django import forms
from django.forms import widgets
from django.forms.widgets import RadioSelect

from .models import (
    Persona,
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

    
class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = [
            'tipo_identificacion',
            'numero_identificacion',
            'nombre_persona',
            'apellido_paterno',
            'apellido_materno',
            'fecha_nacimiento',
            'direccion_persona',
            'numero_direccion',
            'complemento_direccion',
            'telefono_persona',
            'correo_persona',
        ]
        widgets = {
            'tipo_identificacion': RadioSelect(),
            'fecha_nacimiento' : DateInput(),
        }