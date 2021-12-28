from django import forms
from .models import (
    CargaEntregasPandemia,
    CargaEmpresas,
    CargaPatentesVehiculares,
    CargaPermisosCirculacion,
    CargaDOM,
    CargaExencionAseo,
)


class CargaEntregaPandemiaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CargaEntregaPandemiaForm,self).__init__(*args, **kwargs)

    class Meta:
        model = CargaEntregasPandemia
        fields = ['carga_producto']
        labels = {
            'carga_producto': 'Excel Entrega Pandemia',
        }

class CargaEmpresasForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CargaEmpresasForm,self).__init__(*args, **kwargs)

    class Meta:
        model = CargaEmpresas
        fields = ['carga_producto']
        labels = {
            'carga_producto': 'Excel Empresas',
        }

class CargaPatentesVehicularesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CargaPatentesVehicularesForm,self).__init__(*args, **kwargs)

    class Meta:
        model = CargaPatentesVehiculares
        fields = ['carga_producto']
        labels = {
            'carga_producto': 'Excel Patentes Vehiculares',
        }

class CargaPermisosCirculacionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CargaPermisosCirculacionForm,self).__init__(*args, **kwargs)

    class Meta:
        model = CargaPermisosCirculacion
        fields = ['carga_producto']
        labels = {
            'carga_producto': 'Excel Permisos Circulacion',
        }

class CargaDOMForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CargaDOMForm,self).__init__(*args, **kwargs)

    class Meta:
        model = CargaDOM
        fields = ['carga_producto']
        labels = {
            'carga_producto': 'Excel DOM',
        }

class CargaExencionAseoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CargaExencionAseoForm,self).__init__(*args, **kwargs)

    class Meta:
        model = CargaExencionAseo
        fields = ['carga_producto']
        labels = {
            'carga_producto': 'Excel Exencion Aseo',
        }