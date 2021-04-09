from django.contrib import admin
from import_export import resources
from .models import (
    FormularioOMIL,
    CallesCondiciones,
    Paises,
    Seguridad,
)

class FormularioOMILExport(resources.ModelResource):

    class Meta:
        model = FormularioOMIL

class FormularioOMILAdmin(admin.ModelAdmin):
    readonly_fields = ('created','updated','autor')

class FormularioSeguridadAdmin(admin.ModelAdmin):
    readonly_fields = ('created','updated','autor')

class CallesCondicionesAdmin(admin.ModelAdmin):
    readonly_fields = ('calle','condiciones')

class PaisesAdmin(admin.ModelAdmin):
    readonly_fields = ['nombre']

admin.site.register(FormularioOMIL,FormularioOMILAdmin)
admin.site.register(CallesCondiciones,CallesCondicionesAdmin)
admin.site.register(Paises,PaisesAdmin)
admin.site.register(Seguridad,FormularioSeguridadAdmin)


