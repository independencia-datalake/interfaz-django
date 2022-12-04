from ast import NotIn
from unicodedata import name
from django import forms
from .models import (
    ProductoFarmacia,
    BodegaVirtual,
    ProductoIngresado,
    ProductoMermado,
)
from django.forms import inlineformset_factory
from django.forms.widgets import (
    RadioSelect,
)


class BodegaVirtualForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(BodegaVirtualForm,self).__init__(*args, **kwargs)
        # var = self.fields['nombre']
        # var.disabled = True

    class Meta:
        model = BodegaVirtual
        fields = [
            'nombre',
            'stock',
            'stock_min',
            'stock_max',
        ]
        widgets = {
             'nombre': forms.Select(attrs={'style': 'width: 670px','readonly':True}),
             'stock': forms.NumberInput(attrs={'style': 'width: 670px','min':0}),
             'stock_min': forms.NumberInput(attrs={'style': 'width: 670px', 'min':0}),
             'stock_max': forms.NumberInput(attrs={'style': 'width: 670px','min':0}),
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
            'stock',
            'stock_min',
            'stock_max',
        ]
        widgets = {
             'nombre': forms.Select(attrs={'style': 'width: 670px'}),
             'stock': forms.NumberInput(attrs={'style': 'width: 670px','min':0}),
             'stock_min': forms.NumberInput(attrs={'style': 'width: 670px', 'min':0}),
             'stock_max': forms.NumberInput(attrs={'style': 'width: 670px','min':0}),
            }
class BodegaVirtualsalidaForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(BodegaVirtualsalidaForm,self).__init__(*args, **kwargs)
        nombre_ids = BodegaVirtual.objects.values_list('nombre_id', flat=True)
        self.fields['nombre'].queryset = ProductoFarmacia.objects.filter(id__in=nombre_ids)
        
    class Meta:
        model = ProductoMermado
        fields = [
            'nombre',
            'cantidad',
            'motivo',
        ]
        widgets = {
             'nombre': forms.Select(attrs={'style': 'width: 670px'}),
             'cantidad': forms.NumberInput(attrs={'style': 'width: 670px','min':0}),
             'motivo': RadioSelect(),
            }
class BodegaVirtualIngresoProductoForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(BodegaVirtualIngresoProductoForm,self).__init__(*args, **kwargs)
        nombre_ids = BodegaVirtual.objects.values_list('nombre_id', flat=True)
        self.fields['nombre'].queryset = ProductoFarmacia.objects.filter(id__in=nombre_ids)        


    class Meta:
        model = ProductoIngresado
        fields = [
            'nombre',
            'cantidad',
            'precio_compra',
            'precio_venta',
            'lote',
            'n_factura'
            # 'laboratorio',
            # 'cenabast',
            # 'proveedor',
        ]
        widgets = {
            #  'nombre': forms.Select(attrs={'style': 'width: 670px'}),
             'cantidad': forms.NumberInput(attrs={'min':1}),
             'precio_compra': forms.NumberInput(attrs={'min':0}),
            #  'laboratorio': forms.Select(attrs={'style': 'width: 670px'}),
            #  'proveedor': forms.TextInput(attrs={'size':84}),
            }

class BodegaVirtualIngresoStockForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(BodegaVirtualIngresoStockForm,self).__init__(*args, **kwargs)
    class Meta:
        model = BodegaVirtual
        fields = [
            'stock_min',
        ]
        