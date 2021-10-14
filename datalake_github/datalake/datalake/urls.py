"""django_project URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #ADMIN
    path('admin/', admin.site.urls),
    #CORE
    path('', include('core.urls')),
    #USUARIO
    path('usuario/', include('users.urls')),
    #FARMACIA
    path('farmacia/', include('farmacia.urls')),
    #FORMULARIO
    path('formularios/', include('formulario.urls')),
    #CALCULADORA DE UV
    path('calculadora/', include('calculadorauv.urls')),
    #VISUALIZACION
    path('vis/', include('vis.urls')),
    #DIMAP
    path('dimap/', include('dimap.urls')),
    #SEGURIDAD MUNICIPAL
    path('seguridad/', include('seguridad.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
