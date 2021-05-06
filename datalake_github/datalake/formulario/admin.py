from django.contrib import admin
from import_export import resources
from .models import *

#EXPORTAR MODELOS PARA LA VISUALIZACION

class FormularioBaseExport(resources.ModelResource):

    class Meta:
        model = FormularioBase

class DenunciaExport(resources.ModelResource):

    class Meta:
        model = Denuncia

class ControlDePlagaExport(resources.ModelResource):

    class Meta:
        model = ControlDePlaga

class EsterilizacionExport(resources.ModelResource):

    class Meta:
        model = Esterilizacion

#ADMIN

class FormularioBaseAdmin(admin.ModelAdmin):
    readonly_fields = ('created','updated','autor')

class DenunciaAdmin(admin.ModelAdmin):
    readonly_fields = ('created','updated','autor')

class ControlDePlagaAdmin(admin.ModelAdmin):
    readonly_fields = ('created','updated','autor')

class EsterilizacionAdmin(admin.ModelAdmin):
    readonly_fields = ('created','updated','autor')

class CallesCondicionesAdmin(admin.ModelAdmin):
    readonly_fields = ('calle','condiciones')

class PaisesAdmin(admin.ModelAdmin):
    readonly_fields = ['nombre']

admin.site.register(FormularioBase,FormularioBaseAdmin)
admin.site.register(Denuncia,DenunciaAdmin)
admin.site.register(ControlDePlaga,ControlDePlagaAdmin)
admin.site.register(Esterilizacion,EsterilizacionAdmin)
admin.site.register(CallesCondiciones,CallesCondicionesAdmin)
admin.site.register(Paises,PaisesAdmin)


