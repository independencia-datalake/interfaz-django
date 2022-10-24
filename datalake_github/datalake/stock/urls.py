from django.urls import path
from django.views.generic import TemplateView
from . import views
from .views import (

    #STOCK
    InicioStock,
    EdicionStock,
    createStock,
)

urlpatterns = [
    # path('',TemplateView.as_view(template_name='farmacia/homefarmacia.html'),name="farmacia-home"),

    #STOCK DE LA FARMACIA
    path('StockTest/',createStock.as_view()),
    path('',InicioStock.as_view(), name="Stock-inicio"),
    path('crear/', views.crear_producto_Stock, name='productostock-create'),
    path('<int:pk>/edicion/',EdicionStock.as_view(),name="Stock-update"),
    path('Stock2/',views.Stocks, name='Stock-2'),
]