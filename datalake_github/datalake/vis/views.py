import pandas as pd
import os
import boto3
import json

from django.shortcuts import render, redirect

from .forms import(FiltroTiempo)
from core.models import(UV,Direccion,Persona)
from farmacia.models import(ComprobanteVenta)
from dimap.models import(ControlPlaga,Procedimiento,SeguridadDIMAP)
from seguridad.models import(Requerimiento)
from carga.models import(EntregasPandemia)


#CONFIGURACION DEL S3 AWS
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')


def vis(request):
    return render(request,'vis/index.html')


def inicio_vis(request):
    uv = UV.objects.all()

    #return render(request,'vis/inicio_vis.html')
    context = {
        'uv':uv
    }

    return render(request,'vis/home_vis.html', context)


def farmacia_vis(request):

    filtro_tiempo=FiltroTiempo()

    if request.method == 'GET':

        diccionario_tabla = {}
        query_tabla = '''select cu.numero_uv as id, f.cant
                    from core_uv cu
                    left join (select fc.id, cu.numero_uv as uv, count(1) as cant
                        from farmacia_comprobanteventa fc
                        join core_persona cp
                            on fc.comprador_id = cp.id
                        join core_uv cu 
                            on cp.uv_id = cu.id
                        group by cu.numero_uv) f
                        on cu.numero_uv = f.uv;'''        

        for c in ComprobanteVenta.objects.raw(query_tabla):
            diccionario_tabla[c.id] = c.cant

        lista_mapa = []
        query_mapa = '''select u.id, u.numero_uv, fc.created
                        from farmacia_comprobanteventa fc
                        left join core_persona p
                            on fc.comprador_id = p.id
                        left join core_uv u
                            on p.uv_id = u.id 
                        order by fc.created asc;'''

        for c in ComprobanteVenta.objects.raw(query_mapa):
            lista_mapa.append({"uv":c.numero_uv,"created": str(c.created)})

        context = {
            'filtro_tiempo':filtro_tiempo,
            'prueba_diccionario':lista_mapa,
            'diccionario_tabla': diccionario_tabla
        }

        return render(request,'vis/farmacia_vis.html', context)

    elif request.method == 'POST':

        filtro_tiempo=FiltroTiempo(request.POST)
        
        if filtro_tiempo.is_valid():
            fecha_inicio = filtro_tiempo.cleaned_data.get('fecha_inicio')
            fecha_fin = filtro_tiempo.cleaned_data.get('fecha_fin')

            print(fecha_inicio)
            print(fecha_fin)
            
            diccionario_tabla = {}
            query_tabla = f"select cu.numero_uv as id, f.cant \
                    from core_uv cu \
                    left join (select fc.id, cu.numero_uv as uv, count(1) as cant \
                        from farmacia_comprobanteventa fc \
                        join core_persona cp \
                            on fc.comprador_id = cp.id \
                        join core_uv cu \
                            on cp.uv_id = cu.id \
                        where fc.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                        group by cu.numero_uv) f \
                        on cu.numero_uv = f.uv;"

            for c in ComprobanteVenta.objects.raw(query_tabla):
                diccionario_tabla[c.id] = c.cant

            lista_mapa = []
            query_mapa = f"select fc.id, p.nombre_persona ,u.numero_uv, fc.created \
                            from farmacia_comprobanteventa fc \
                            left join core_persona p \
                                on fc.comprador_id = p.id \
                            left join core_uv u \
                                on p.uv_id = u.id \
                            where fc.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            order by fc.created asc;"

            for r in ComprobanteVenta.objects.raw(query_mapa):

                lista_mapa.append({"uv":r.numero_uv,"created": str(r.created)})

            context = {
                'filtro_tiempo':filtro_tiempo,
                'diccionario_tabla': diccionario_tabla,
                'prueba_diccionario': lista_mapa
            }
            
            return render(request,'vis/farmacia_vis.html', context)


#DIMAP HIGIENE
def dimap_vis(request):
    
    filtro_tiempo=FiltroTiempo()

    if request.method == 'GET':

        diccionario_tabla = {}
        query_tabla = '''select cu.numero_uv as id, f.cant
                        from core_uv cu
                        left join (select dc.id, cu.numero_uv as uv, count(1) as cant
                        from dimap_controlplaga dc
                        join core_persona cp
                            on dc.persona_id = cp.id
                        join core_uv cu 
                            on cp.uv_id = cu.id
                        group by cu.numero_uv) f
                        on cu.numero_uv = f.uv;'''

        for c in ControlPlaga.objects.raw(query_tabla):
            diccionario_tabla[c.id] = c.cant
        
        print(diccionario_tabla)

        lista_mapa = []
        query_mapa = '''select dc.id, cu.numero_uv as uc, dc.created
                        from dimap_controlplaga dc
                        left join core_persona cp 
                            on dc.persona_id = cp.id
                        left join core_uv cu
                            on cp.uv_id = cu.id
                        where cu.numero_uv <> 0
                        order by dc.created asc;'''
        
        for c in ControlPlaga.objects.raw(query_mapa):
            lista_mapa.append({"uv":c.numero_uv,"created": str(c.created)})

        context = {
            'filtro_tiempo':filtro_tiempo,
            'prueba_diccionario': lista_mapa,
            'diccionario_tabla': diccionario_tabla
        }

        return render(request,'vis/farmacia_vis.html', context)

    elif request.method == 'POST':

        uv = UV.objects.all()
        control_de_plaga = ControlPlaga.objects.all()
        seguridad_dimap = SeguridadDIMAP.objects.all()
        esterilizacion = Procedimiento.objects.all()

        context = {
            'uv':uv
        }

        return render(request,'vis/dimap_vis.html', context)

