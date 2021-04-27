from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView
from formulario.models import *
from django.contrib.auth.admin import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

class ListaFormularioBase(ListView):
  model = FormularioBase
  template_name = 'core/home.html'
  context_object_name = 'formularios'
  ordering = ['-created']

def quienes(request):

  return render(request,"core/quienes.html")

def qya(request):

  return render(request,"core/qya.html")

