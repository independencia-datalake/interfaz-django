import pandas as pd
from django.shortcuts import render
from core.models import CallesIndependencia
from django.http import JsonResponse

from ayuda_funciones.uv import obtener_uv

def calculadorauv(request):   
    return render(request, 'calculadorauv/calculadora_uv.html')

def cal_uv(request):
    nombre_calle = request.GET['nombre_calle']
    numero_calle = int(request.GET['numero_calle'])
    uv=obtener_uv(nombre_calle,numero_calle)

    context = {
        'uv':uv,
    }

    return render(request,'calculadorauv/calculadora_uv.html',context)

#AUTOCOMPLETADO
def autocompete_calles(request):
  if 'term' in request.GET:
      qs = CallesIndependencia.objects.filter(calle__icontains=request.GET.get('term'))
      calles = list()
      for calle in qs:
          calles.append(calle.calle)
      return JsonResponse(calles, safe=False)