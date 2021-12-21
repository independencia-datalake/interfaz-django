import django_filters
from django.contrib.auth.models import User
from django_filters.filters import (
    ChoiceFilter,
)

from core.models import (
    Persona,
    Direccion,
)
from .models import (
    Procedimiento,
    ControlPlaga,
    SeguridadDIMAP,
)


class ProcedimientoFilter(django_filters.FilterSet):

    autor_filtro = django_filters.ModelChoiceFilter(field_name='autor',lookup_expr='exact',queryset=User.objects.all(),)


    class Meta:
        model = Procedimiento
        fields = {
            'estatus',
        }

class ControlPlagaFilter(django_filters.FilterSet):

    persona_filtro = django_filters.ModelChoiceFilter(field_name='persona',lookup_expr='exact',queryset=Persona.objects.all(),)
    autor_filtro = django_filters.ModelChoiceFilter(field_name='autor',lookup_expr='exact',queryset=User.objects.all(),)


    class Meta:
        model = ControlPlaga
        fields = {
            'estatus',
        }

class SeguridadDIMAPFilter(django_filters.FilterSet):

    persona_filtro = django_filters.ModelChoiceFilter(field_name='persona',lookup_expr='exact',queryset=Persona.objects.all(),)
    autor_filtro = django_filters.ModelChoiceFilter(field_name='autor',lookup_expr='exact',queryset=User.objects.all(),)

    class Meta:
        model = SeguridadDIMAP
        fields = {
            'estatus',
            'tipo_denuncia',
            'l_transgrsion',
            'i_visita',
            'notificacion',
        }