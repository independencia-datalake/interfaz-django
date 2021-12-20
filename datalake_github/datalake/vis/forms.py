from django import forms
from django.forms import widgets
from django.forms.fields import CharField

class FiltroTiempo(forms.Form):
    fecha_inicio = forms.DateField(
        input_formats=['%Y-%m-%d','%m/%d/%Y','%m/%d/%y'],
        widget = forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }
                )
    )
    fecha_fin = forms.DateField(
        input_formats=['%Y-%m-%d','%m/%d/%Y','%m/%d/%y'],
        widget = forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }
                )
    )
