from django.contrib.auth.models import User
import django_filters
from core.models import(
    Persona,
)
from .models import (
    ComprobanteVenta,
    ProductoFarmacia,
    BodegaVirtual,
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
    # numero_identificacion_filtro = django_filters.CharFilter(label='Número de Identidad',field_name='comprador',lookup_expr='icontains')
    comprador_filtro = django_filters.ModelChoiceFilter(field_name='comprador',lookup_expr='exact',queryset=Persona.objects.all(),)
    farmaceuta_filtro = django_filters.ModelChoiceFilter(field_name='farmaceuta',lookup_expr='exact',queryset=User.objects.all(),)

    class Meta:
        model = ComprobanteVenta
        fields = {
        }
    
class Stockfilter(django_filters.FilterSet):
    OPCIONES = (
        ('ascendente','Ascendente'),
        ('descendente','Descendente'),
    )
    nombre_filtro = django_filters.CharFilter(label='Marca del Producto',field_name='nombre__marca_producto',lookup_expr='contains')
    # Stock_filtro = django_filters.CharFilter(label='Stock',field_name='Stock',lookup_expr='contains')
    ordering = django_filters.ChoiceFilter(label='Orden por holgura', choices=OPCIONES, method='filter_by_order')

    class Meta:
        model = BodegaVirtual
        fields = {
        }
    
    def filter_by_order(self, queryset, name, value):
        expression = 'holgura' if value == 'ascendente' else '-holgura'
        return queryset.order_by(expression)