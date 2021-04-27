from django import forms
from django.contrib.auth.models import User
from .models import *
from django.forms import formset_factory

class ComprobanteForm(forms.ModelForm):
    

    class Meta:
        model = ComprobanteVenta
        fields = ['numero_identificacion', 'farmaceuta']

class ProductoVendidoForm(forms.ModelForm):

    class Meta:
        model = ProductoVendido
        fields = ['nombre', 'cantidad', 'n_venta', 'farmaceuta']
