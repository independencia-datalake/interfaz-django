from django.urls import path
from . import views
from .views import (
    CrearFormularioOMIL,
    DetalleFormularioOMIL,
    EdicionFormularioOMIL,
    CrearSeguridad,
    DetalleSeguridad,
    EdicionSeguridad,
    CrearFarmacia,
    DetalleFarmacia,
    EdicionFarmacia,
)

urlpatterns = [
    #FORMULARIO OMIL
    path('formularioOMIL/', CrearFormularioOMIL.as_view(), name='formularioomil-create'),
    path('formularioOMIL/<int:pk>/',DetalleFormularioOMIL.as_view(),name="formularioomil-detail"),
    path('formularioOMIL/<int:pk>/edicion/',EdicionFormularioOMIL.as_view(),name="formularioomil-update"),
    #FORMULARIO SEGURIDAD
    path('formularioSeguridad/', CrearSeguridad.as_view(), name='seguridad-create'),
    path('formularioSeguridad/<int:pk>/',DetalleSeguridad.as_view(),name="seguridad-detail"),
    path('formularioSeguridad/<int:pk>/edicion/',EdicionSeguridad.as_view(),name="seguridad-update"),
    #FORMULARIO FARMACIA
    path('formularioFarmacia/', CrearFarmacia.as_view(), name='farmacia-create'),
    path('formularioFarmacia/<int:pk>/',DetalleFarmacia.as_view(),name="farmacia-detail"),
    path('formularioFarmacia/<int:pk>/edicion/',EdicionFarmacia.as_view(),name="farmacia-update"),
    #AUTOCOMPLETADO
    path('autocompletado-calles',views.autocompete_calles, name='autocompete_calles'),
    path('autocompletado-paises',views.autocompete_pais, name='autocompete_pais'),
]