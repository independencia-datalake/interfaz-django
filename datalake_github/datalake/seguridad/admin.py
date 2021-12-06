from django.contrib import admin
from .models import(
    Requerimiento,
)

#CREATED Y UPDETED SOLO DE LECTURA
class RequerimientoAdmin(admin.ModelAdmin):
    readonly_fields = ['created','updated']

#PERMITE QUE SE VEA EN EL ADMIN
admin.site.register(Requerimiento, RequerimientoAdmin)