from django import forms
from django.db.models.fields import CharField
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
            'presentacion',
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
        fields = ['receta']




#     comprador = models.ForeignKey(Persona, on_delete=models.PROTECT,verbose_name='Comprador') 
#     receta = models.ImageField(default='default.jpg', upload_to='receta_medica')
#     farmaceuta = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Profesional')
#     created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación", editable=False)
#     updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición", editable=False)



class ComprobanteVentaModelForm(forms.ModelForm):
    # title = forms.CharField()
    class Meta:
        model = ComprobanteVenta
        fields = [
            'receta'
            ]
        labels = {
            'receta':"Receta Medica"
        }
    
    # def __init__(self, *args, **kwargs):
    #     super(ComprobanteVentaModelForm, self).__init__(*args, **kwargs)
    #     self.fields['receta'].widget = forms.ClearableFileInput()


    # def clean_title(self, *args, **kwargs):
    #     title = self.cleaned_data.get('title')
    #     return title

    # def clean_receta(self, *args, **kwargs):
    #     receta = self.cleaned_data.get('receta')
    #     print(receta)
    #     return receta


        
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
