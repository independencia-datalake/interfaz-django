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

    def __init__(self, data=None, *args, **kwargs):
        # if filterset is bound, use initial values as defaults
        if data is not None:
            # get a mutable copy of the QueryDict
            data = data.copy()

            for name, f in self.base_filters.items():
                initial = f.extra.get('choices')

                # filter param is either missing or empty, use initial as default
                if not data.get(name) and name == 'estatus':
                    data[name] = initial[2][0]

        super().__init__(data, *args, **kwargs)