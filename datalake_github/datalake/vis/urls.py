from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    #path('', TemplateView.as_view(template_name='vis/home_vis.html'), name='inicio-vis'),
    path('', views.inicio_vis, name="inicio-vis"),
    path('dimap/<int:categoria>', views.dimap_vis, name='dimap-vis'),
    path('farmacia/', views.farmacia_vis, name='farmacia-vis'),
    path('impuestosyderechos/<int:categoria>', views.impuestos_derechos_vis, name='impuestos-vis'),
    path('transito/<int:categoria>', views.transito_vis, name='transito-vis'),
    path('seguridad/<int:categoria>', views.seguridad_vis, name='seguridad-vis'),
    path('ayudapandemia/<int:categoria>', views.entrega_pandemia_vis, name='ayudapandemia-vis'),
    path('obrasmunicipales/<int:categoria>', views.obras_municipales_vis, name='obrasmunicipales-vis'),   
    path('excencionbasura/<int:categoria>', views.exencion_vis, name='excencionbasura-vis'),    
]    