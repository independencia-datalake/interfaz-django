from django.contrib.auth.models import User
import django_filters
from core.models import(
    Persona,
    PersonaInfoSalud,
)
from .models import (
    ComprobanteVenta,
    ProductoFarmacia,
    ProductoVendido,
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
    comprador_nombre_filtro = django_filters.CharFilter(label="Nombre Persona", field_name='comprador__nombre_completo', lookup_expr='icontains')
    farmaceuta_filtro = django_filters.ModelChoiceFilter(field_name='farmaceuta',lookup_expr='exact',queryset=User.objects.all(),)

    class Meta:
        model = ComprobanteVenta
        fields = {
        }

class ProductosVendidosFilter(django_filters.FilterSet):
    OPCIONES = (
        ('ascendente','Ascendente'),
        ('descendente','Descendente'),
    )
    marca_producto_filtro = django_filters.CharFilter(label='Nombre Producto',field_name='nombre',lookup_expr='icontains')
    n_venta_filtro = django_filters.CharFilter(label='Numero de venta',field_name='n_venta',lookup_expr='icontains')
    ordering = django_filters.ChoiceFilter(label='Orden por precio', choices=OPCIONES, method='filter_by_order')

    class Meta:
        model = ProductoVendido
        fields = {
        }
    
    def filter_by_order(self, queryset, name, value):
        expression = 'precio' if value == 'ascendente' else '-precio'
        return queryset.order_by(expression)

class PersonaInfoSaludFilter(django_filters.FilterSet):
    OPCIONES = (
        ('ascendente','Ascendente'),
        ('descendente','Descendente'),
    )
    
    nombre_filtro = django_filters.CharFilter(label="Nombre Persona", field_name='persona__nombre_completo', lookup_expr='icontains')
    persona_filtro = django_filters.CharFilter(label="Rut Persona", field_name='persona__numero_identificacion', lookup_expr='icontains')
    prevision_filtro = django_filters.CharFilter(label="Prevision", field_name='prevision', lookup_expr='icontains') 
    isapre_filtro =  django_filters.CharFilter(label="Isapre", field_name='isapre', lookup_expr='icontains')
    ordering = django_filters.ChoiceFilter(label='Orden por rut', choices=OPCIONES, method='filter_by_order')

    class Meta:
        model = PersonaInfoSalud
        fields = {

        }
    def filter_by_order(self, queryset, name, value):
        expression = 'persona' if value == 'ascendente' else '-persona'
        return queryset.order_by(expression)
