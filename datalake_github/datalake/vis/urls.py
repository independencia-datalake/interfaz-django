from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_vis, name='inicio-vis'),
    path('vis/', views.vis, name='vis'),
]    