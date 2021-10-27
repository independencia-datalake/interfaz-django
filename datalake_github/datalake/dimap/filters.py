from django.contrib.auth.models import User
import django_filters

from core.models import (
    UV,
)
from .models import (
    Esterilizacion
)

class EsterilizacionFilter(django_filters.FilterSet):
    nombre_responsable_filtro = django_filters.CharFilter(label='Nombre del Responsable',field_name='nombre_responsable',lookup_expr='icontains')
    autor_filtro = django_filters.ModelChoiceFilter(field_name='autor',lookup_expr='exact',queryset=User.objects.all(),)
    uv = django_filters.ModelChoiceFilter(field_name='uv',lookup_expr='exact',queryset=UV.objects.all(),)

    class Meta:
        model = Esterilizacion
        fields = {
        }