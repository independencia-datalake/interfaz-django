from django import forms
from .models import (
    EntregasPandemia,
    Empresas,
    PatentesVehiculares,
    PermisosCirculacion,    
)


class CargaEntregaPandemiaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CargaEntregaPandemiaForm,self).__init__(*args, **kwargs)

    class Meta:
        model = EntregasPandemia
        fields = ['carga_producto']
        labels = {
            'carga_producto': 'Excel Entrega Pandemia',
        }

class CargaEmpresasForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CargaEmpresasForm,self).__init__(*args, **kwargs)

    class Meta:
        model = Empresas
        fields = ['carga_producto']
        labels = {
            'carga_producto': 'Excel Empresas',
        }

class CargaPatentesVehicularesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CargaPatentesVehicularesForm,self).__init__(*args, **kwargs)

    class Meta:
        model = PatentesVehiculares
        fields = ['carga_producto']
        labels = {
            'carga_producto': 'Excel Patentes Vehiculares',
        }

class CargaPermisosCirculacionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CargaPermisosCirculacionForm,self).__init__(*args, **kwargs)

    class Meta:
        model = PermisosCirculacion
        fields = ['carga_producto']
        labels = {
            'carga_producto': 'Excel Permisos Circulacion',
        }