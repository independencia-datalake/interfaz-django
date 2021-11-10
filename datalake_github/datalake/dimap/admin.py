from django.contrib import admin
from .models import(
    Procedimiento,
    Mascota,
    ControlPlaga,
)

#CREATED Y UPDETED SOLO DE LECTURA
class ProcedimientoAdmin(admin.ModelAdmin):
    readonly_fields = ['created','updated']

class MascotaAdmin(admin.ModelAdmin):
    readonly_fields = ['created','updated']

class ControlPlagaAdmin(admin.ModelAdmin):
    readonly_fields = ['created','updated']

#PERMITE QUE SE VEA EN EL ADMIN
admin.site.register(Procedimiento, ProcedimientoAdmin)
admin.site.register(Mascota, MascotaAdmin)
admin.site.register(ControlPlaga, ControlPlagaAdmin)
