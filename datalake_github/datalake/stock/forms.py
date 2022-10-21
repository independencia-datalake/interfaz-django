from ast import NotIn
from unicodedata import name
from django import forms
from .models import (
    ProductoFarmacia,
    ComprobanteVenta,
    ProductoVendido,
    CargaProducto,
    BodegaVirtual,
)
from django.forms import inlineformset_factory
from django.forms.widgets import (
    RadioSelect,
)


class BodegaVirtualForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(BodegaVirtualForm,self).__init__(*args, **kwargs)
        var = self.fields['nombre']
        var.disabled = True

    class Meta:
        model = BodegaVirtual
        fields = [
            'nombre',
            'Stock',
            'Stock_min',
            'Stock_max',
        ]
        widgets = {
             'nombre': forms.Select(attrs={'style': 'width: 670px','readonly':True}),
             'Stock': forms.NumberInput(attrs={'style': 'width: 670px','min':0}),
             'Stock_min': forms.NumberInput(attrs={'style': 'width: 670px', 'min':0}),
             'Stock_max': forms.NumberInput(attrs={'style': 'width: 670px','min':0}),
            }
class BodegaVirtualcrearForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(BodegaVirtualcrearForm,self).__init__(*args, **kwargs)
        nombre_ids = BodegaVirtual.objects.values_list('nombre_id', flat=True)
        self.fields['nombre'].queryset = ProductoFarmacia.objects.exclude(id__in=nombre_ids)
        
    class Meta:
        model = BodegaVirtual
        fields = [
            'nombre',
            'Stock',
            'Stock_min',
            'Stock_max',
        ]
        widgets = {
             'nombre': forms.Select(attrs={'style': 'width: 670px'}),
             'Stock': forms.NumberInput(attrs={'style': 'width: 670px','min':0}),
             'Stock_min': forms.NumberInput(attrs={'style': 'width: 670px', 'min':0}),
             'Stock_max': forms.NumberInput(attrs={'style': 'width: 670px','min':0}),
            }

