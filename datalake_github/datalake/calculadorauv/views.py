import pandas as pd
from django.shortcuts import render
from core.models import CallesIndependencia
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


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

def obtener_uv(calle, numero):
  df = pd.read_csv('calculadorauv/static/calculadorauv/streets_uv.csv')
  validaciones = df[df['calle']==calle]
  uv = None

  for index, row in validaciones.iterrows():
    if row['condicion'] == 'PAR':
      uv = validar_par(numero, row)
    elif row['condicion'] == 'IMPAR':
      uv = validar_impar(numero, row)
    elif row['condicion'] == 'NO':
      uv = row['uv']
    elif row['condicion'] == 'MENOR':
      uv = validar_menor(numero,row)
    elif row['condicion'] == 'MAYOR':
      uv = validar_mayor(numero,row)
    elif row['condicion'] == 'ENTRE':
      uv = validar_entre(numero,row)
    elif row['condicion'] == 'PARMENOR':
      uv = validar_parmenor(numero,row)
    elif row['condicion'] == 'IMPARMENOR':
      uv = validar_imparmenor(numero,row)
    elif row['condicion'] == 'CONJUNTO':
      uv = validar_conjunto(numero,row)  
    if uv != None:
      return uv

def validar_par(numero, validacion):
  if numero % 2 == 0:
    return validacion['uv']

def validar_impar(numero, validacion):
  if numero % 2 != 0:
    return validacion['uv']

def validar_menor(numero, validacion):
  if numero < int(validacion['conjunto']):
    return validacion['uv']

def validar_mayor(numero, validacion):
  if numero > int(validacion['conjunto']):
    return validacion['uv']

def validar_entre(numero, validacion):
  lim_inf = int(validacion['conjunto'].split('-')[0])
  lim_sup = int(validacion['conjunto'].split('-')[1])
  if numero > lim_inf and numero < lim_sup:
      return validacion['uv']

def validar_parmenor(numero, validacion):
  if numero % 2 == 0 and numero < int(validacion['conjunto']):
    return validacion['uv']

def validar_imparmenor(numero, validacion):
  if numero % 2 != 0 and numero < int(validacion['conjunto']):
    return validacion['uv']

def validar_conjunto(numero, validacion):
  conjunto = validacion['conjunto'].replace('(','')
  conjunto = conjunto.replace(')','')
  conjunto = conjunto.split(' ')
  if str(numero) in conjunto:
    return validacion['uv']

#AUTOCOMPLETADO

def autocompete_calles(request):
    if 'term' in request.GET:
        qs = CallesIndependencia.objects.filter(calle__contains=request.GET.get('term'))
        calles = list()
        for calle in qs:
            calles.append(calle.calle)
        return JsonResponse(calles, safe=False)