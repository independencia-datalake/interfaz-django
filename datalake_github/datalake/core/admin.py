from django.contrib import admin
from .models import (
    CallesIndependencia,
    Persona,
    UV,
)

#QUE LAS CALLES SEAN SOLO DE LECTURA
class CallesIndependenciaAdmin(admin.ModelAdmin):
    readonly_fields = ['calle']
#QUE LAS UNIDADES VECINALES SEAN SOLO DE LECTURA
class UVAdmin(admin.ModelAdmin):
    readonly_fields = ['numero_uv']
#QUE LAS UNIDADES VECINALES SEAN SOLO DE LECTURA
class PersonaAdmin(admin.ModelAdmin):
    readonly_fields = ['uv','created','updated']

#PERMITE QUE SE VEA EN EL ADMIN
admin.site.register(CallesIndependencia, CallesIndependenciaAdmin)
admin.site.register(Persona, PersonaAdmin)
admin.site.register(UV, UVAdmin)

