from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView
from formulario.models import *
from django.contrib.auth.admin import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def paginaprincipal(request):

  fb_form = FormularioBase.objects.filter(autor=request.user)
  d_form = Denuncia.objects.filter(autor=request.user)
  cdp_form = ControlDePlaga.objects.filter(autor=request.user)
  e_form = Esterilizacion.objects.filter(autor=request.user)
  filtro = "inicio"
  if request.GET:
    filtro = request.GET['nombre_formulario']

  context = {
    'fb_form': fb_form,
    'd_form': d_form,
    'cdp_form': cdp_form,
    'e_form': e_form,
    'filtro':filtro
  }

  return render(request, "core/home.html",context)

def quienes(request):

  return render(request,"core/quienes.html")

def qya(request):

  return render(request,"core/qya.html")

