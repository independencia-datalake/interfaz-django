from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='vis/home_vis.html'), name='inicio-vis'),
    path('dimap/<int:categoria>', views.dimap_vis, name='dimap-vis'),
    path('farmacia/', views.farmacia_vis, name='farmacia-vis'),
    path('impuestosyderechos/', views.farmacia_vis, name='impuestos-vis'),
    path('transito/', views.farmacia_vis, name='transito-vis'),
    path('seguridad/<int:categoria>', views.seguridad_vis, name='seguridad-vis'),
    path('ayudapandemia/', views.farmacia_vis, name='ayudapandemia-vis'),
    path('obrasmunicipales/', views.farmacia_vis, name='obrasmunicipales-vis'),    
]    