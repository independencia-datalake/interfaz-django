from ast import NotIn
from unicodedata import name
from django import forms
from .models import (
    ProductoFarmacia,
    ComprobanteVenta,
    ProductoVendido,
    CargaProducto,
)
from stock.models import BodegaVirtual
from core.models import PersonaInfoSalud
from django.forms import inlineformset_factory
from django.forms.widgets import (
    RadioSelect,
)

class ProductoFarmaciaForm(forms.ModelForm): 
    laboratorio = forms.CharField(max_length= 200)
    def __init__(self, *args, **kwargs):
        super(ProductoFarmaciaForm,self).__init__(*args, **kwargs)

    class Meta:
        
        model = ProductoFarmacia
        fields = [
            'marca_producto',
            'p_a',
            'dosis',
            'presentacion',
            'bioequivalencia',
            'cenabast',
            'proveedor',
            'laboratorio',
        ]
        widgets = {
            'f_ven' : forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }
                ),
        }

class ProductoFarmaciaModelForm(forms.ModelForm): #se agrega precio para la edicion
    laboratorio = forms.CharField(max_length= 200)
    def __init__(self, *args, **kwargs):
        super(ProductoFarmaciaModelForm,self).__init__(*args, **kwargs)

    class Meta:
        
        model = ProductoFarmacia
        fields = [
            'marca_producto',
            'p_a',
            'dosis',
            'presentacion',
            'precio',
            'bioequivalencia',
            'cenabast',
            'proveedor',
            'laboratorio',
        ]
        widgets = {
            'f_ven' : forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Select a date',
                    'type': 'date'
                    }
                ),
        }


class ComprobanteVentaModelForm(forms.ModelForm):
    # receta = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}))

    class Meta:
        model = ComprobanteVenta
        fields = [
            # 'receta'
            ]
        # labels = {
        #     'receta':"Receta Medica"
        # }

        
class ProductoVendidoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductoVendidoForm,self).__init__(*args, **kwargs)
        # self.fields['nombre'].queryset = ProductoFarmacia.objects.filter(active=True)
        nombre_ids = BodegaVirtual.objects.values_list('nombre_id', flat=True)
        self.fields['nombre'].queryset = ProductoFarmacia.objects.filter(id__in=nombre_ids)

    class Meta:
        model = ProductoVendido
        fields = ['nombre', 'cantidad']

class ProductoVendidoEdicionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductoVendidoEdicionForm,self).__init__(*args, **kwargs)
        # self.fields['nombre'].queryset = ProductoFarmacia.objects.filter(active=True)
        var = self.fields['nombre']
        var.disabled = True
        self.fields['cantidad']

    class Meta:
        model = ProductoVendido
        fields = ['nombre', 'cantidad']


ProductoVendidoFormset = inlineformset_factory(ComprobanteVenta,
                                                ProductoVendido,
                                                form=ProductoVendidoForm,
                                                can_delete=False,
                                                extra=1)



class CargaProductoModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CargaProductoModelForm,self).__init__(*args, **kwargs)
        

    class Meta:
        model = CargaProducto
        fields = ['carga_producto']
        labels = {
            'carga_producto': 'Excel Productos Farmacia',
        }

class ProductoVendidoInformeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductoVendidoInformeForm,self).__init__(*args, **kwargs)
        self.fields['nombre'].queryset = ProductoFarmacia.objects.all()

    class Meta:
        model = ProductoVendido
        fields = ['nombre']

class PersonaInfoSaludEdicionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonaInfoSaludEdicionForm,self).__init__(*args, **kwargs)
        # self.fields['nombre'].queryset = ProductoFarmacia.objects.filter(active=True)
        var = self.fields['persona']
        var.disabled = True
        self.fields['prevision']
        self.fields['isapre']
        self.fields['comentarios']

    class Meta:
        model = PersonaInfoSalud
        fields = ['persona', 'prevision','isapre','comentarios']