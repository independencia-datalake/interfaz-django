from django.contrib.auth.models import User
import django_filters

from core.models import (
    Persona,
    Direccion,
)
from .models import (
    Procedimiento,
    ControlPlaga,
)

class ProcedimientoFilter(django_filters.FilterSet):

    autor_filtro = django_filters.ModelChoiceFilter(field_name='autor',lookup_expr='exact',queryset=User.objects.all(),)


    class Meta:
        model = Procedimiento
        fields = {
        }

class ControlPlagaFilter(django_filters.FilterSet):

    persona_filtro = django_filters.ModelChoiceFilter(field_name='persona',lookup_expr='exact',queryset=Persona.objects.all(),)
    autor_filtro = django_filters.ModelChoiceFilter(field_name='autor',lookup_expr='exact',queryset=User.objects.all(),)


    class Meta:
        model = ControlPlaga
        fields = {
        }