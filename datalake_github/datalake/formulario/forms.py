from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from .models import *
from django.utils.timezone import localdate

class DateInput(forms.DateInput):
    input_type = 'date'

#FORMULARIO BASE
class FormularioBaseForm(forms.ModelForm):
    
    class Meta:
        model = FormularioBase
        fields = [
                'p_origen',
                'tipo_identificacion',
                'numero_identificacion',
                'nombre',
                'apellido',
                'direccion',
                'numero_calle',
                'texto1',
                'texto2',
                'texto3',
                'texto4',
                ]

#DENUNCIA
class DenunciaForm(forms.ModelForm):

    class Meta:
        model = Denuncia
        fields = [
                'estatus',
                'tipo_identificacion_denunciante',
                'numero_identificacion_denunciante',
                'nombre_denunciante',
                'apellido_p_denunciante',
                'apellido_m_denunciante',
                'telefono_denunciante',
                'direccion',
                'numero_calle',
                'email_denunciante',
                'tipo_denuncia',
                'texto_denuncia',
                'nombre_denunciado',
                'apellido_p_denunciado',
                'apellido_m_denunciado',
                'telefono_denunciado',
                'direccion_denunciado',
                'numero_calle_denunciado',
                'email_denunciado',
                'fecha_visita',
                'lugar_de_transgresion',
                'visita_inspectiva',
                'texto_observacion',
                'categoria_visita',
                'notificacion',
                'numero_noficacion',
                'texto_enviado',
                'ver_respuesta',
                ]
        widgets = {
            'fecha_visita' : DateInput(),
        }

#CONTROL DE PLAGA
class ControlDePlagaForm(forms.ModelForm):
    
    class Meta:
        model = ControlDePlaga
        fields = [
            'estatus',
            'ficha_numero',
            'tipo_identificacion',
            'numero_identificacion',
            'nombre',
            'apellido_p',
            'apellido_m',
            'telefono',
            'direccion',
            'numero_calle',
            'email',
            'tipo_solicitud',
            'fecha_coordinada',
            'jornada',
            'fecha_visita',
            'producto',
            ]
        widgets = {
            'fecha_coordinada' : DateInput(),
            'fecha_visita' : DateInput(),
        }

#ESTERILIZACION
class EsterilizacionForm(forms.ModelForm):

    class Meta:
        model = Esterilizacion
        fields = [
            'estatus',
            'tipo_identificacion',
            'numero_identificacion',
            'nombre',
            'apellido_p',
            'apellido_m',
            'telefono',
            'direccion',
            'numero_calle',
            'email',
            'mascota',
            'nombre_mascota',
            'sexo_mascota',
            'fecha_cirugia',
            'clinica',
            'asistencia',
            'rechazo',
            ]
        widgets = {
            'fecha_cirugia' : DateInput()
        }