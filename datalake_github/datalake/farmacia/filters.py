from django.contrib.auth.models import User
import django_filters
from .models import (
    ComprobanteVenta,
    ProductoFarmacia,
)

class ProductoFarmaciaFilter(django_filters.FilterSet):
    OPCIONES = (
        ('ascendente','Ascendente'),
        ('descendente','Descendente'),
    )
    marca_producto_filtro = django_filters.CharFilter(label='Nombre Producto',field_name='marca_producto',lookup_expr='icontains')
    p_a_filtro = django_filters.CharFilter(label='Componente Activo',field_name='p_a',lookup_expr='icontains')
    dosis_filtro = django_filters.CharFilter(label='Dosis',field_name='dosis',lookup_expr='icontains')
    ordering = django_filters.ChoiceFilter(label='Orden por precio', choices=OPCIONES, method='filter_by_order')

    class Meta:
        model = ProductoFarmacia
        fields = {
        }
    
    def filter_by_order(self, queryset, name, value):
        expression = 'precio' if value == 'ascendente' else '-precio'
        return queryset.order_by(expression)

class ComprobanteVentaFilter(django_filters.FilterSet):
    numero_identificacion_filtro = django_filters.CharFilter(label='Número de Identidad',field_name='numero_identificacion',lookup_expr='icontains')
    farmaceuta_filtro = django_filters.ModelChoiceFilter(field_name='farmaceuta',lookup_expr='exact',queryset=User.objects.all(),)

    class Meta:
        model = ComprobanteVenta
        fields = {
        }