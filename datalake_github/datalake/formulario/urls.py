from django.urls import path
from . import views
from .views import (
    InicioFormularioBase,
    CrearFormularioBase,
    DetalleFormularioBase,
    EdicionFormularioBase,
)
from .views import *

urlpatterns = [
    #FORMULARIO BASE
    path('formularioBase/', InicioFormularioBase.as_view(), name='formulariobase-inicio'),
    path('formularioBase/crear/', CrearFormularioBase.as_view(), name='formulariobase-create'),
    path('formularioBase/<int:pk>/',DetalleFormularioBase.as_view(),name="formulariobase-detail"),
    path('formularioBase/<int:pk>/edicion/',EdicionFormularioBase.as_view(),name="formulariobase-update"),
    #DENUNCIA
    path('Denuncia/', InicioDenuncia.as_view(), name='denuncia-inicio'),
    path('Denuncia/crear/', CrearDenuncia.as_view(), name='denuncia-create'),
    path('Denuncia/<int:pk>/',DetalleDenuncia.as_view(),name="denuncia-detail"),
    path('Denuncia/<int:pk>/edicion/',EdicionDenuncia.as_view(),name="denuncia-update"),
    #CONTROL DE PLAGA
    path('ControlDePlaga/', InicioControlDePlaga.as_view(), name='controldeplaga-inicio'),
    path('ControlDePlaga/crear/', CrearControlDePlaga.as_view(), name='controldeplaga-create'),
    path('ControlDePlaga/<int:pk>/',DetalleControlDePlaga.as_view(),name="controldeplaga-detail"),
    path('ControlDePlaga/<int:pk>/edicion/',EdicionControlDePlaga.as_view(),name="controldeplaga-update"),
    #ESTERILIZACION
    path('Esterilizacion/', InicioEsterilizacion.as_view(), name='esterilizacion-inicio'),
    path('Esterilizacion/crear/', CrearEsterilizacion.as_view(), name='esterilizacion-create'),
    path('Esterilizacion/<int:pk>/',DetalleEsterilizacion.as_view(),name="esterilizacion-detail"),
    path('Esterilizacion/<int:pk>/edicion/',EdicionEsterilizacion.as_view(),name="esterilizacion-update"),
]