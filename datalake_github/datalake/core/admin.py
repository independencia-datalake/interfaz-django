from django.contrib import admin
from .models import (
    CallesIndependencia,
    Persona,
    UV,
)

#QUE LAS CALLES SEAN SOLO UN ARCHIVO DE LECTURA
class CallesIndependenciaAdmin(admin.ModelAdmin):
    readonly_fields = ['calle']

#PERMITE QUE SE VEA EN EL ADMIN
admin.site.register(CallesIndependencia, CallesIndependenciaAdmin)
admin.site.register(Persona)
admin.site.register(UV)

