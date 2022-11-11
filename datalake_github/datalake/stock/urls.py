from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import (

    #STOCK
    InicioStock,
    EdicionStock,
)

urlpatterns = [
    # path('',TemplateView.as_view(template_name='farmacia/homefarmacia.html'),name="farmacia-home"),

    #STOCK DE LA FARMACIA
    path('',InicioStock.as_view(), name="Stock-inicio"),
    path('Inicio/',views.HomeStock, name='Stock-home'),
    path('crear/', views.crear_producto_Stock, name='productostock-create'),
    path('<int:pk>/edicion/',EdicionStock.as_view(),name="Stock-update"),
    path('Salida/', views.salida_producto_stock, name='productostock-salida'),
    path('Ingreso/', views.ingreso_producto_stock, name='productostock-ingreso'),
]