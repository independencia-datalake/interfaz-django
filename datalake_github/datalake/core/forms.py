from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import(
    AutocompleteSelect,
)
from django.forms.widgets import (
    RadioSelect,
)
from farmacia.models import ComprobanteVenta
from .models import (
    CallesIndependencia,
    Persona,
    Telefono,
    Correo,
    Direccion,
    PersonaInfoSalud,
    PersonaArchivos,
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
    numero_identificacion = forms.CharField(max_length=200, label='Número de identificación')                  
 
class PersonaModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonaModelForm,self).__init__(*args, **kwargs)

    class Meta:
        model = Persona
        fields = [
            'tipo_identificacion',
            'numero_identificacion',
            'nacionalidad',
            'nombre_persona',
            'apellido_paterno',
            'apellido_materno',
            'fecha_nacimiento',
            'estado_civil',
            'hijos',
            'enfermedad',
            'medicamento',
            'lugar_de_atencion',
            'discapacidad',
            'certificado_compin',
            'embarazo',
            'certificado_embarazo',
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
            'tipo_telefono_secundario',
            'telefono_secundario',
        ]
        widgets = {
            'tipo_telefono': RadioSelect(),
            'tipo_telefono_secundario': RadioSelect(),
        }

class CorreoModelForm(forms.ModelForm):
    class Meta:
        model = Correo
        fields = [
            'correo',
        ]


class DireccionModelForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = [
            'calle',
            'numero',
            'complemento_direccion',
        ]

class PersonaInfoSaludModelForm(forms.ModelForm):

    class Meta:
        model = PersonaInfoSalud
        fields = [
            'prevision',
            'isapre',
            'comentarios',
        ]
        widgets = {
            'prevision' : forms.RadioSelect(),
            'isapre': forms.Select(),
            'comentarios': forms.Textarea(
                attrs={
                    'rows': 4, 
                    }
                ),
        }
    def clean(self):
        data = super().clean()
        prevision = self.cleaned_data.get('prevision')
        isapre = self.cleaned_data.get('isapre')
        if prevision == 'ISAPRE' and isapre == 'NO APLICA':
            raise forms.ValidationError('Seleccione una Prevision valida porfavor \n O en su defecto una Isapre Valida ')
        return data

class PersonaArchivosModelForm(forms.ModelForm):

    class Meta:
        model = PersonaArchivos
        fields = [
            # 'archivo',
        ]