from django import forms
from .models import (
    ProductoFarmacia,
    ComprobanteVenta,
    ProductoVendido,
    CargaProducto,
)
from django.forms import inlineformset_factory
from django.forms.widgets import (
    RadioSelect,
)


class ProductoFarmaciaForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(ProductoFarmaciaForm,self).__init__(*args, **kwargs)

    class Meta:
        model = ProductoFarmacia
        fields = [
            'active',
            'marca_producto',
            'p_a',
            'dosis',
            'presentacion',
            'f_ven',
            'precio',
            'n_lote',
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
    class Meta:
        model = ComprobanteVenta
        fields = [
            'receta'
            ]
        labels = {
            'receta':"Receta Medica"
        }

        
class ProductoVendidoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductoVendidoForm,self).__init__(*args, **kwargs)
        self.fields['nombre'].queryset = ProductoFarmacia.objects.filter(active=True)

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