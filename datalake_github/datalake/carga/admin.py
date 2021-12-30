from django.contrib import admin
from .models import(
    EntregasPandemia,
    Empresas,
    PermisosCirculacion,
    PatentesVehiculares,
    DOM,
    ExencionAseo,
)

admin.site.register(EntregasPandemia)
admin.site.register(Empresas)
admin.site.register(PermisosCirculacion)
admin.site.register(PatentesVehiculares)
admin.site.register(DOM)
admin.site.register(ExencionAseo)
