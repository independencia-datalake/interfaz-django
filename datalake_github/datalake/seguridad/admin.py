from django.contrib import admin
from .models import(
    ClasificacionDelito,
    Delito,
    Requerimiento,
)

#CREATED Y UPDETED SOLO DE LECTURA
class RequerimientoAdmin(admin.ModelAdmin):
    readonly_fields = ['numero_requerimiento','uv','created','updated','autor']

#PERMITE QUE SE VEA EN EL ADMIN
admin.site.register(Requerimiento, RequerimientoAdmin)
admin.site.register(ClasificacionDelito)
admin.site.register(Delito)