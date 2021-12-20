import pandas as pd
import os
import json

from django.shortcuts import render, redirect

from .forms import(FiltroTiempo)
from farmacia.models import(ComprobanteVenta)
from dimap.models import(ControlPlaga,Procedimiento,SeguridadDIMAP)
from seguridad.models import(Requerimiento)
from carga.models import(EntregasPandemia, PatentesVehiculares,PermisosCirculacion,Empresas)

# #CONFIGURACION DEL S3 AWS
# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')

#FARMACIA
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
            'lista_mapa':lista_mapa,
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
                'lista_mapa': lista_mapa
            }
            
            return render(request,'vis/farmacia_vis.html', context)

#DIMAP HIGIENE
def dimap_vis(request,categoria):
    
    filtro_tiempo=FiltroTiempo()
    filtro_mapa = ["total","control de plaga","esterilizacion","denuncia"]

    if request.method == 'GET':


        #CONTROL DE PLAGA

        diccionario_tabla_controldeplaga = {}
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
            diccionario_tabla_controldeplaga[c.id] = c.cant

        lista_mapa_controldeplaga = []
        query_mapa = '''select dc.id, cu.numero_uv as uc, dc.created
                        from dimap_controlplaga dc
                        left join core_persona cp 
                            on dc.persona_id = cp.id
                        left join core_uv cu
                            on cp.uv_id = cu.id
                        where cu.numero_uv <> 0
                        order by dc.created asc;'''
        
        for c in ControlPlaga.objects.raw(query_mapa):
            lista_mapa_controldeplaga.append({"uv":c.uv.numero_uv,"created": str(c.created)})

        

        # ESTERILIZACION

        # diccionario_tabla_esterilizacion = {}
        # query_tabla = '''select *
        #                 from dimap_procedimiento dp
        #                 left join dimap_mascota dm 
        #                     on dp.mascota_id = dm.id
        #                 left join core_persona cp
        #                     on dm.persona_id = cp.id
        #                 left join core_uv cu
        #                     on cp.uv_id = cu.id
        #                 where cu.numero_uv <> 0
        #                 order by dm.created asc;'''

        # for c in Procedimiento.objects.raw(query_tabla):
        #     diccionario_tabla_esterilizacion[c.id] = c.cant

        lista_mapa_esterilizacion = []
        query_mapa = '''select *
                        from dimap_procedimiento dp
                        left join dimap_mascota dm 
                            on dp.mascota_id = dm.id
                        left join core_persona cp
                            on dm.persona_id = cp.id
                        left join core_uv cu
                            on cp.uv_id = cu.id
                        where cu.numero_uv <> 0
                        order by dm.created asc;'''
        
        for c in Procedimiento.objects.raw(query_mapa):
            lista_mapa_esterilizacion.append({"uv":c.numero_uv,"created": str(c.created)})


        # DENUNCIA

        # diccionario_tabla_seguridad = {}
        # query_tabla = '''select *
        #                 from dimap_seguridaddimap ds 
        #                 left join core_persona cp 
        #                     on ds.persona_id = cp.id
        #                 left join core_uv cu
        #                     on cp.uv_id = cu.id
        #                 where cu.numero_uv <> 0
        #                 order by ds.created asc;'''

        # for c in SeguridadDIMAP.objects.raw(query_tabla):
        #     diccionario_tabla_seguridad[c.id] = c.cant

        lista_mapa_seguridad = []
        query_mapa = '''select *
                        from dimap_seguridaddimap ds 
                        left join core_persona cp 
                            on ds.persona_id = cp.id
                        left join core_uv cu
                            on cp.uv_id = cu.id
                        where cu.numero_uv <> 0
                        order by ds.created asc;'''
        
        for c in SeguridadDIMAP.objects.raw(query_mapa):
            lista_mapa_seguridad.append({"uv":c.numero_uv,"created": str(c.created)})

        #TOTAL FINAL
        diccionario_tabla_total = diccionario_tabla_controldeplaga
        lista_mapa_total = []
        for obj in lista_mapa_seguridad:
            lista_mapa_total.append(obj)
        for obj in lista_mapa_controldeplaga:
            lista_mapa_total.append(obj)
        for obj in lista_mapa_esterilizacion:
            lista_mapa_total.append(obj)

        print(lista_mapa_total)

        filtro_categoria  = categoria
        filtro_categoria 

        if filtro_mapa[filtro_categoria] == "control de plaga":
            lista_mapa = lista_mapa_controldeplaga
        elif filtro_mapa[filtro_categoria] == "esterilizacion":
            lista_mapa = lista_mapa_esterilizacion
        elif filtro_mapa[filtro_categoria] == "denuncia":
            lista_mapa = lista_mapa_seguridad
        elif filtro_mapa[filtro_categoria] == "total":
            lista_mapa = lista_mapa_total

        diccionario_tabla = diccionario_tabla_total
        print(diccionario_tabla)

        context = {
            'filtro_tiempo':filtro_tiempo,
            'lista_mapa': lista_mapa,
            'diccionario_tabla': diccionario_tabla,
        }

        return render(request,'vis/dimap_vis.html', context)

    if request.method == 'POST':
        filtro_tiempo=FiltroTiempo(request.POST)
        
        if filtro_tiempo.is_valid():
            fecha_inicio = filtro_tiempo.cleaned_data.get('fecha_inicio')
            fecha_fin = filtro_tiempo.cleaned_data.get('fecha_fin')

        #CONTROL DE PLAGA

        diccionario_tabla_controldeplaga = {}
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
            diccionario_tabla_controldeplaga[c.id] = c.cant

        lista_mapa_controldeplaga = []
        query_mapa = '''select dc.id, cu.numero_uv as uc, dc.created
                        from dimap_controlplaga dc
                        left join core_persona cp 
                            on dc.persona_id = cp.id
                        left join core_uv cu
                            on cp.uv_id = cu.id
                        where cu.numero_uv <> 0
                        order by dc.created asc;'''
        
        for c in ControlPlaga.objects.raw(query_mapa):
            lista_mapa_controldeplaga.append({"uv":c.uv.numero_uv,"created": str(c.created)})

        

        # ESTERILIZACION

        # diccionario_tabla_esterilizacion = {}
        # query_tabla = '''select *
        #                 from dimap_procedimiento dp
        #                 left join dimap_mascota dm 
        #                     on dp.mascota_id = dm.id
        #                 left join core_persona cp
        #                     on dm.persona_id = cp.id
        #                 left join core_uv cu
        #                     on cp.uv_id = cu.id
        #                 where cu.numero_uv <> 0
        #                 order by dm.created asc;'''

        # for c in Procedimiento.objects.raw(query_tabla):
        #     diccionario_tabla_esterilizacion[c.id] = c.cant

        lista_mapa_esterilizacion = []
        query_mapa = '''select *
                        from dimap_procedimiento dp
                        left join dimap_mascota dm 
                            on dp.mascota_id = dm.id
                        left join core_persona cp
                            on dm.persona_id = cp.id
                        left join core_uv cu
                            on cp.uv_id = cu.id
                        where cu.numero_uv <> 0
                        order by dm.created asc;'''
        
        for c in Procedimiento.objects.raw(query_mapa):
            lista_mapa_esterilizacion.append({"uv":c.numero_uv,"created": str(c.created)})


        # DENUNCIA

        # diccionario_tabla_seguridad = {}
        # query_tabla = '''select *
        #                 from dimap_seguridaddimap ds 
        #                 left join core_persona cp 
        #                     on ds.persona_id = cp.id
        #                 left join core_uv cu
        #                     on cp.uv_id = cu.id
        #                 where cu.numero_uv <> 0
        #                 order by ds.created asc;'''

        # for c in SeguridadDIMAP.objects.raw(query_tabla):
        #     diccionario_tabla_seguridad[c.id] = c.cant

        lista_mapa_seguridad = []
        query_mapa = '''select *
                        from dimap_seguridaddimap ds 
                        left join core_persona cp 
                            on ds.persona_id = cp.id
                        left join core_uv cu
                            on cp.uv_id = cu.id
                        where cu.numero_uv <> 0
                        order by ds.created asc;'''
        
        for c in SeguridadDIMAP.objects.raw(query_mapa):
            lista_mapa_seguridad.append({"uv":c.numero_uv,"created": str(c.created)})

        #TOTAL FINAL
        diccionario_tabla_total = diccionario_tabla_controldeplaga
        lista_mapa_total = []
        for obj in lista_mapa_seguridad:
            lista_mapa_total.append(obj)
        for obj in lista_mapa_controldeplaga:
            lista_mapa_total.append(obj)
        for obj in lista_mapa_esterilizacion:
            lista_mapa_total.append(obj)

        print(lista_mapa_total)

        filtro_categoria  = categoria
        filtro_categoria 

        if filtro_mapa[filtro_categoria] == "control de plaga":
            lista_mapa = lista_mapa_controldeplaga
        elif filtro_mapa[filtro_categoria] == "esterilizacion":
            lista_mapa = lista_mapa_esterilizacion
        elif filtro_mapa[filtro_categoria] == "denuncia":
            lista_mapa = lista_mapa_seguridad
        elif filtro_mapa[filtro_categoria] == "total":
            lista_mapa = lista_mapa_total

        diccionario_tabla = diccionario_tabla_total
        print(diccionario_tabla)

        context = {
            'filtro_tiempo':filtro_tiempo,
            'lista_mapa': lista_mapa,
            'diccionario_tabla': diccionario_tabla,
        }

        return render(request,'vis/dimap_vis.html', context)

#SEGURIDAD MUNICIPAL
def seguridad_vis(request, categoria):
    filtro_tiempo=FiltroTiempo()
    filtro_mapa = [
        "Total",
        "Delito de mayor connotacion social",
        "Violencia Intrafamiliar",
        "Incivilidades",
        "Abusos sexuales",
        "Accidentes e incendios",
        "Derivaciones",
        "Otro",
    ]

    if request.method == 'GET':


        # #SEGURIDAD MUNICIPAL

        # diccionario_tabla_seguridad_municipal = {}
        # query_tabla = '''select cu.numero_uv as id, f.cant
        #                 from core_uv cu
        #                 left join (select dc.id, cu.numero_uv as uv, count(1) as cant
        #                 from dimap_controlplaga dc
        #                 join core_persona cp
        #                     on dc.persona_id = cp.id
        #                 join core_uv cu 
        #                     on cp.uv_id = cu.id
        #                 group by cu.numero_uv) f
        #                 on cu.numero_uv = f.uv;'''

        # for c in Requerimiento.objects.raw(query_tabla):
        #     diccionario_tabla_seguridad_municipal[c.id] = c.cant

        # lista_mapa_seguridad_municipal = []
        # query_mapa = '''select dc.id, cu.numero_uv as uc, dc.created
        #                 from dimap_controlplaga dc
        #                 left join core_persona cp 
        #                     on dc.persona_id = cp.id
        #                 left join core_uv cu
        #                     on cp.uv_id = cu.id
        #                 where cu.numero_uv <> 0
        #                 order by dc.created asc;'''
        
        # for c in Requerimiento.objects.raw(query_mapa):
        #     lista_mapa_seguridad_municipal.append({"uv":c.uv.numero_uv,"created": str(c.created)})

        
        #TOTAL FINAL
        diccionario_tabla_total = {}
        lista_mapa_total = []
        # for obj in lista_mapa_seguridad:
        #     lista_mapa_total.append(obj)
        # for obj in lista_mapa_controldeplaga:
        #     lista_mapa_total.append(obj)
        # for obj in lista_mapa_esterilizacion:
        #     lista_mapa_total.append(obj)

        if filtro_mapa[categoria] == "Total":
            lista_mapa = lista_mapa_total
        # elif filtro_mapa[categoria] == "Delito de mayor connotacion social":
        #     lista_mapa = 
        # elif filtro_mapa[categoria] == "Violencia Intrafamiliar":
        #     lista_mapa = 
        # elif filtro_mapa[categoria] == "Incivilidades":
        #     lista_mapa = 
        # elif filtro_mapa[categoria] == "Abusos sexuales":
        #     lista_mapa = 
        # elif filtro_mapa[categoria] == "Accidentes e incendios":
        #     lista_mapa = 
        # elif filtro_mapa[categoria] == "Derivaciones":
        #     lista_mapa = 
        # elif filtro_mapa[categoria] == "Otro":
        #     lista_mapa = 

        print(diccionario_tabla_total)

        context = {
            'filtro_tiempo':filtro_tiempo,
            'lista_mapa': lista_mapa,
            'diccionario_tabla': diccionario_tabla_total,
        }

        return render(request,'vis/seguridad_vis.html', context)

    if request.method == 'POST':
        filtro_tiempo=FiltroTiempo(request.POST)
        
        if filtro_tiempo.is_valid():
            fecha_inicio = filtro_tiempo.cleaned_data.get('fecha_inicio')
            fecha_fin = filtro_tiempo.cleaned_data.get('fecha_fin')

        # #SEGURIDAD MUNICIPAL

        # diccionario_tabla_seguridad_municipal = {}
        # query_tabla = '''select cu.numero_uv as id, f.cant
        #                 from core_uv cu
        #                 left join (select dc.id, cu.numero_uv as uv, count(1) as cant
        #                 from dimap_controlplaga dc
        #                 join core_persona cp
        #                     on dc.persona_id = cp.id
        #                 join core_uv cu 
        #                     on cp.uv_id = cu.id
        #                 group by cu.numero_uv) f
        #                 on cu.numero_uv = f.uv;'''

        # for c in Requerimiento.objects.raw(query_tabla):
        #     diccionario_tabla_seguridad_municipal[c.id] = c.cant

        # lista_mapa_seguridad_municipal = []
        # query_mapa = '''select dc.id, cu.numero_uv as uc, dc.created
        #                 from dimap_controlplaga dc
        #                 left join core_persona cp 
        #                     on dc.persona_id = cp.id
        #                 left join core_uv cu
        #                     on cp.uv_id = cu.id
        #                 where cu.numero_uv <> 0
        #                 order by dc.created asc;'''
        
        # for c in Requerimiento.objects.raw(query_mapa):
        #     lista_mapa_seguridad_municipal.append({"uv":c.uv.numero_uv,"created": str(c.created)})

        
        #TOTAL FINAL
        diccionario_tabla_total = {}
        lista_mapa_total = []
        # for obj in lista_mapa_seguridad:
        #     lista_mapa_total.append(obj)
        # for obj in lista_mapa_controldeplaga:
        #     lista_mapa_total.append(obj)
        # for obj in lista_mapa_esterilizacion:
        #     lista_mapa_total.append(obj)

        if filtro_mapa[categoria] == "Total":
            lista_mapa = lista_mapa_total
        # elif filtro_mapa[categoria] == "Delito de mayor connotacion social":
        #     lista_mapa = 
        # elif filtro_mapa[categoria] == "Violencia Intrafamiliar":
        #     lista_mapa = 
        # elif filtro_mapa[categoria] == "Incivilidades":
        #     lista_mapa = 
        # elif filtro_mapa[categoria] == "Abusos sexuales":
        #     lista_mapa = 
        # elif filtro_mapa[categoria] == "Accidentes e incendios":
        #     lista_mapa = 
        # elif filtro_mapa[categoria] == "Derivaciones":
        #     lista_mapa = 
        # elif filtro_mapa[categoria] == "Otro":
        #     lista_mapa = 

        print(diccionario_tabla_total)

        context = {
            'filtro_tiempo':filtro_tiempo,
            'lista_mapa': lista_mapa,
            'diccionario_tabla': diccionario_tabla_total,
        }

        return render(request,'vis/seguridad_vis.html', context)