from django.contrib.auth.models import User
import django_filters
from core.models import(
    Persona,
)
from .models import (
    ProductoFarmacia,
    BodegaVirtual,
)

class Stockfilter(django_filters.FilterSet):
    OPCIONES = (
        ('ascendente','Ascendente'),
        ('descendente','Descendente'),
    )
    nombre_filtro = django_filters.CharFilter(label='Marca del Producto',field_name='nombre__marca_producto',lookup_expr='icontains')
    # Stock_filtro = django_filters.CharFilter(label='Stock',field_name='Stock',lookup_expr='contains')
    ordering = django_filters.ChoiceFilter(label='Orden por holgura', choices=OPCIONES, method='filter_by_order')

    class Meta:
        model = BodegaVirtual
        fields = {
        }
    
    def filter_by_order(self, queryset, name, value):
        expression = 'holgura' if value == 'ascendente' else '-holgura'
        return queryset.order_by(expression)