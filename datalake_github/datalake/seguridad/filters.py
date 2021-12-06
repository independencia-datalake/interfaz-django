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
    Requerimiento,
)


class RequerimientoFilter(django_filters.FilterSet):

    autor_filtro = django_filters.ModelChoiceFilter(field_name='autor',lookup_expr='exact',queryset=User.objects.all(),)

    class Meta:
        model = Requerimiento
        fields = {
            'estatus',
        }
