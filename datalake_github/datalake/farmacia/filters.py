import django_filters
from .models import (
    ProductoFarmacia
)

class ProductofarmaciaFilter(django_filters.FilterSet):
    OPCIONES = (
        ('ascendente','Ascendente'),
        ('descendente','Descendente'),
    )
    ordering = django_filters.ChoiceFilter(label='Orden por precio', choices=OPCIONES, method='filter_by_order')

    class Meta:
        model = ProductoFarmacia
        fields = {
            'marca_producto' : ['icontains'],
            'p_a' : ['icontains'],
            'dosis' : ['icontains'],
        }
    
    def filter_by_order(self, queryset, name, value):
        expression = 'precio' if value == 'ascendente' else '-precio'
        return queryset.order_by(expression)