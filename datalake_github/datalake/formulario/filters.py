import django_filters
from .models import (
    FormularioBase,
    Denuncia,
    ControlDePlaga,
    Esterilizacion,
)

#FILTRO FORMULARIO BASE
class FormularioBaseFilter(django_filters.FilterSet):
    OPCIONES = (
        ('ascendente','Ascendente'),
        ('descendente','Descendente'),
    )
    ordering = django_filters.ChoiceFilter(label='Orden', choices=OPCIONES, method='filter_by_order')

    class Meta:
        model = FormularioBase
        fields = {
            'numero_identificacion' : ['icontains'],
            'apellido' : ['icontains'],
            'autor' : ['exact'],
        }
    
    def filter_by_order(self, queryset, name, value):
        expression = 'created' if value == 'ascendente' else '-created'
        return queryset.order_by(expression)

#FILTRO DENUNCIA
class DenunciaFilter(django_filters.FilterSet):
    ESTATUS = (
        ('Pendiente','Pendiente'),
        ('realizado','Realizado'),
    )
    estatus = django_filters.ChoiceFilter(label='Estatus', choices=ESTATUS)

    OPCIONES = (
        ('ascendente','Ascendente'),
        ('descendente','Descendente'),
    )
    ordering = django_filters.ChoiceFilter(label='Orden', choices=OPCIONES, method='filter_by_order')
   
    class Meta:
        model = Denuncia
        fields = {
            'numero_identificacion_denunciante' : ['icontains'],
            'autor' : ['exact'],
        }
    
    def filter_by_order(self, queryset, name, value):
        expression = 'created' if value == 'ascendente' else '-created'
        return queryset.order_by(expression)


#FILTRO CONTROL DE PLAGA
class ControlDePlagaFilter(django_filters.FilterSet):
    ESTATUS = (
        ('Pendiente','Pendiente'),
        ('realizado','Realizado'),
    )
    estatus = django_filters.ChoiceFilter(label='Estatus', choices=ESTATUS)

    OPCIONES = (
        ('ascendente','Ascendente'),
        ('descendente','Descendente'),
    )

    ordering = django_filters.ChoiceFilter(label='Orden', choices=OPCIONES, method='filter_by_order')

    class Meta:
        model = ControlDePlaga
        fields = {
            'numero_identificacion' : ['icontains'],
            'autor' : ['exact'],
        }
    
    def filter_by_order(self, queryset, name, value):
        expression = 'created' if value == 'ascendente' else '-created'
        return queryset.order_by(expression)


#FILTRO ESTERILIZACION
class EsterilizacionFilter(django_filters.FilterSet):
    ESTATUS = (
        ('Pendiente','Pendiente'),
        ('realizado','Realizado'),
    )
    estatus = django_filters.ChoiceFilter(label='Estatus', choices=ESTATUS)

    OPCIONES = (
        ('ascendente','Ascendente'),
        ('descendente','Descendente'),
    )

    ordering = django_filters.ChoiceFilter(label='Orden', choices=OPCIONES, method='filter_by_order')

    class Meta:
        model = Esterilizacion
        fields = {
            'numero_identificacion' : ['icontains'],
            'autor' : ['exact'],
        }
    
    def filter_by_order(self, queryset, name, value):
        expression = 'created' if value == 'ascendente' else '-created'
        return queryset.order_by(expression)