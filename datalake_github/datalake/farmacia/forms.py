from django import forms
from .models import (
    ProductoFarmacia,
    ComprobanteVenta,
    ProductoVendido,
)
from django.forms import inlineformset_factory
from django.forms.widgets import (
    RadioSelect,
)

class DateInput(forms.DateInput):
    input_type = 'date'
    

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
            'precentacion',
            'f_ven',
            'precio',
            'n_lote',
        ]
        widgets = {
            'f_ven' : forms.DateInput()
        }


class ComprobanteVentaForm(forms.ModelForm):
    class Meta:
        model = ComprobanteVenta
        fields = ['tipo_identificacion','numero_identificacion','receta']
        widgets = {
            'tipo_identificacion': RadioSelect(),
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
