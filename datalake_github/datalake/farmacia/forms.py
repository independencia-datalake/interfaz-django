from django import forms
from django.contrib.auth.models import User
from .models import *
from django.forms import inlineformset_factory

class ComprobanteForm(forms.ModelForm):
    

    class Meta:
        model = ComprobanteVenta
        fields = ['numero_identificacion']

class ProductoVendidoForm(forms.ModelForm):

    class Meta:
        model = ProductoVendido
        fields = ['nombre', 'cantidad']
ProductoVendidoFormset = inlineformset_factory(ComprobanteVenta,ProductoVendido,form=ProductoVendidoForm, extra=10)