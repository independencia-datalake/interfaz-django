from django import forms
from django.contrib.auth.models import User
from .models import *
from django.forms import inlineformset_factory, widgets
from django.utils.timezone import localdate

class DateInput(forms.DateInput):
    input_type = 'date'

class ProductoFarmaciaForm(forms.ModelForm): 

    class Meta:
        model = ProductoFarmacia
        fields = [
            'marca_producto',
            'p_a',
            'dosis',
            'precentacion',
            'f_ven',
            'precio',
            'n_lote',
        ]
        widgets = {
            'f_ven' : DateInput()
        }

class ComprobanteForm(forms.ModelForm):
    
    class Meta:
        model = ComprobanteVenta
        fields = ['numero_identificacion']

class ProductoVendidoForm(forms.ModelForm):

    class Meta:
        model = ProductoVendido
        fields = ['nombre', 'cantidad']
ProductoVendidoFormset = inlineformset_factory(ComprobanteVenta,ProductoVendido,form=ProductoVendidoForm, extra=10)
