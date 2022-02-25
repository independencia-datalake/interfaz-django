from django.contrib import admin
from .models import(
    EntregasPandemia,
    Empresas,
    PermisosCirculacion,
    LicenciaConducir,
    DOM,
    ExencionAseo,
)

admin.site.register(EntregasPandemia)
admin.site.register(Empresas)
admin.site.register(PermisosCirculacion)
admin.site.register(LicenciaConducir)
admin.site.register(DOM)
admin.site.register(ExencionAseo)
