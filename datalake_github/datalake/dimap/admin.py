from django.contrib import admin
from .models import(
    Esterilizacion,
)

#CREATED Y UPDETED SOLO DE LECTURA
class EsterilizacionAdmin(admin.ModelAdmin):
    readonly_fields = ['uv','created','updated']

#PERMITE QUE SE VEA EN EL ADMIN
admin.site.register(Esterilizacion, EsterilizacionAdmin)
