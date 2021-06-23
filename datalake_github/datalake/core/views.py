from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def paginaprincipal(request):
  return render(request, "core/home.html",)

def quienes(request):
  return render(request,"core/quienes.html")

def qya(request):
  return render(request,"core/qya.html")

