import pandas as pd
import os
import json

from django.shortcuts import render, redirect

from .forms import(FiltroTiempo)
from farmacia.models import(ComprobanteVenta)
from dimap.models import(ControlPlaga,Procedimiento,SeguridadDIMAP)
from seguridad.models import(Requerimiento, Delito, ClasificacionDelito)
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
    filtro_mapa = ["total","esterilizacion","denuncia","control de plaga"]

    if request.method == 'GET':
        diccionario_tabla = {}
        query_tabla = '''select cu.numero_uv as id,
                            coalesce(e.esterilizacion, 0) + coalesce(p.higiene, 0) + coalesce(s.seguridad, 0) as total, 
                            case when e.esterilizacion is null then 0 else e.esterilizacion end esterilizacion,
                            case when p.higiene is null then 0 else p.higiene end higiene,
                            case when s.seguridad is null then 0 else s.seguridad end seguridad
                        from core_uv cu
                        left join (select cp.uv_id, count(1) as esterilizacion
                            from dimap_procedimiento dp
                            left join dimap_mascota dm
                                on dp.mascota_id = dm.id
                            left join core_persona cp
                                on dm.persona_id = cp.id
                            group by cp.uv_id) e
                            on cu.id = e.uv_id
                        left join (select cp.uv_id, count(1) as higiene
                            from dimap_controlplaga pl
                            left join core_persona cp
                                on pl.persona_id =  cp.id 
                            group by cp.uv_id) p
                            on cu.id = p.uv_id
                        left join (select cp.uv_id, count(1) as seguridad
                            from dimap_seguridaddimap ds
                            left join core_persona cp
                                on ds.persona_id =  cp.id 
                            group by cp.uv_id) s
                            on cu.id = s.uv_id;'''

        for c in ControlPlaga.objects.raw(query_tabla):
            diccionario_tabla[c.id] = [c.total ,c.esterilizacion,c.seguridad,c.higiene]

        #FILTRO POR CATEGORIA

        if filtro_mapa[categoria] == "control de plaga":
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
                obj = {"uv":c.uv.numero_uv,"created": str(c.created)}
                lista_mapa_controldeplaga.append(obj)
            
            lista_mapa = lista_mapa_controldeplaga

        elif filtro_mapa[categoria] == "esterilizacion":
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
            lista_mapa = lista_mapa_esterilizacion

        elif filtro_mapa[categoria] == "denuncia":
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

            lista_mapa = lista_mapa_seguridad

        elif filtro_mapa[categoria] == "total":
            lista_mapa_total = []
            query_mapa = '''select a.uc as id, a.created from
                            (select cu.numero_uv as uc, dc.created
                            from dimap_controlplaga dc
                            left join core_persona cp 
                                on dc.persona_id = cp.id
                            left join core_uv cu
                                on cp.uv_id = cu.id
                            where cu.numero_uv <> 0
                            union
                            select cu.numero_uv as uv,
                                dp.created
                            from dimap_procedimiento dp
                            left join dimap_mascota dm 
                                on dp.mascota_id = dm.id
                            left join core_persona cp
                                on dm.persona_id = cp.id
                            left join core_uv cu
                                on cp.uv_id = cu.id
                            where cu.numero_uv <> 0
                            union
                            select cu.numero_uv as uv, ds.created
                            from dimap_seguridaddimap ds 
                            left join core_persona cp 
                                on ds.persona_id = cp.id
                            left join core_uv cu
                                on cp.uv_id = cu.id
                            where cu.numero_uv <> 0) a
                            order by created asc'''
        
            for c in SeguridadDIMAP.objects.raw(query_mapa):
                lista_mapa_total.append({"uv":c.id,"created": str(c.created)})

            lista_mapa = lista_mapa_total

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

            diccionario_tabla = {}
            query_tabla = f"select cu.numero_uv as id, \
                                coalesce(e.esterilizacion, 0) + coalesce(p.higiene, 0) + coalesce(s.seguridad, 0) as total, \
                                case when e.esterilizacion is null then 0 else e.esterilizacion end esterilizacion, \
                                case when p.higiene is null then 0 else p.higiene end higiene, \
                                case when s.seguridad is null then 0 else s.seguridad end seguridad \
                            from core_uv cu \
                            left join (select cp.uv_id, count(1) as esterilizacion \
                                from dimap_procedimiento dp \
                                left join dimap_mascota dm \
                                    on dp.mascota_id = dm.id \
                                left join core_persona cp \
                                    on dm.persona_id = cp.id \
                                where dp.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by cp.uv_id) e \
                                on cu.id = e.uv_id \
                            left join (select cp.uv_id, count(1) as higiene \
                                from dimap_controlplaga pl \
                                left join core_persona cp \
                                    on pl.persona_id =  cp.id \
                                where pl.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by cp.uv_id) p \
                                on cu.id = p.uv_id \
                            left join (select cp.uv_id, count(1) as seguridad \
                                from dimap_seguridaddimap ds \
                                left join core_persona cp \
                                    on ds.persona_id =  cp.id \
                                where ds.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by cp.uv_id) s \
                                on cu.id = s.uv_id;"

            for c in ControlPlaga.objects.raw(query_tabla):
                diccionario_tabla[c.id] = [c.total ,c.esterilizacion,c.seguridad,c.higiene]

            #FILTRO POR CATEGORIA

            if filtro_mapa[categoria] == "control de plaga":
                lista_mapa_controldeplaga = []
                query_mapa = f"select dc.id, cu.numero_uv as uc, dc.created \
                                from dimap_controlplaga dc \
                                left join core_persona cp \
                                    on dc.persona_id = cp.id \
                                left join core_uv cu \
                                    on cp.uv_id = cu.id \
                                where cu.numero_uv <> 0 \
                                and dc.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by dc.created asc;"
                
                for c in ControlPlaga.objects.raw(query_mapa):
                    obj = {"uv":c.uv.numero_uv,"created": str(c.created)}
                    lista_mapa_controldeplaga.append(obj)
                
                lista_mapa = lista_mapa_controldeplaga

            elif filtro_mapa[categoria] == "esterilizacion":
                lista_mapa_esterilizacion = []
                query_mapa = f"select * \
                            from dimap_procedimiento dp \
                            left join dimap_mascota dm \
                                on dp.mascota_id = dm.id \
                            left join core_persona cp \
                                on dm.persona_id = cp.id \
                            left join core_uv cu \
                                on cp.uv_id = cu.id \
                            where cu.numero_uv <> 0 \
                            and dm.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            order by dm.created asc;"
            
                for c in Procedimiento.objects.raw(query_mapa):
                    lista_mapa_esterilizacion.append({"uv":c.numero_uv,"created": str(c.created)})
                lista_mapa = lista_mapa_esterilizacion

            elif filtro_mapa[categoria] == "denuncia":
                lista_mapa_seguridad = []
                query_mapa = f"select * \
                            from dimap_seguridaddimap ds \
                            left join core_persona cp \
                                on ds.persona_id = cp.id \
                            left join core_uv cu \
                                on cp.uv_id = cu.id \
                            where cu.numero_uv <> 0 \
                            and ds.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            order by ds.created asc;"
            
                for c in SeguridadDIMAP.objects.raw(query_mapa):
                    lista_mapa_seguridad.append({"uv":c.numero_uv,"created": str(c.created)})

                lista_mapa = lista_mapa_seguridad

            elif filtro_mapa[categoria] == "total":
                lista_mapa_total = []
                query_mapa = f"select a.uc as id, a.created from \
                            (select cu.numero_uv as uc, dc.created \
                            from dimap_controlplaga dc \
                            left join core_persona cp \
                                on dc.persona_id = cp.id \
                            left join core_uv cu \
                                on cp.uv_id = cu.id \
                            where cu.numero_uv <> 0 \
                            and dc.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            union \
                            select cu.numero_uv as uv, \
                                dp.created \
                            from dimap_procedimiento dp \
                            left join dimap_mascota dm \
                                on dp.mascota_id = dm.id \
                            left join core_persona cp \
                                on dm.persona_id = cp.id \
                            left join core_uv cu \
                                on cp.uv_id = cu.id \
                            where cu.numero_uv <> 0 \
                            and dm.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            union \
                            select cu.numero_uv as uv, ds.created \
                            from dimap_seguridaddimap ds \
                            left join core_persona cp \
                                on ds.persona_id = cp.id \
                            left join core_uv cu \
                                on cp.uv_id = cu.id \
                            where cu.numero_uv <> 0 \
                            and ds.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            ) a \
                            order by created asc" 
            
                for c in SeguridadDIMAP.objects.raw(query_mapa):
                    lista_mapa_total.append({"uv":c.id,"created": str(c.created)})

                lista_mapa = lista_mapa_total

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

        diccionario_tabla = {}
        query_tabla = '''select cu.numero_uv as id,
                        coalesce(dm.cant_delito, 0) + coalesce(vif.cant_vif, 0) + coalesce(inc.cant_inc, 0) + coalesce(asx.cant_asx, 0) + coalesce(ai.cant_ai, 0) + coalesce(der.cant_der, 0) + coalesce(otro.cant_otro, 0) total,
                        case when dm.cant_delito is null then 0 else dm.cant_delito end delito,
                        case when vif.cant_vif is null then 0 else vif.cant_vif end vif,
                        case when inc.cant_inc is null then 0 else inc.cant_inc end inc,
                        case when asx.cant_asx is null then 0 else asx.cant_asx end asx,
                        case when ai.cant_ai is null then 0 else ai.cant_ai end ai,
                        case when der.cant_der is null then 0 else der.cant_der end der,
                        case when otro.cant_otro is null then 0 else otro.cant_otro end otro
                        from core_uv cu
                        left join (select sr.uv_id, count(1) as cant_delito
                        from seguridad_requerimiento sr
                        left join seguridad_delito sd
                            on sd.id = sr.delito_id
                        where sd.clasificacion_delito_id = 1
                        group by sr.uv_id) dm
                            on cu.id = dm.uv_id
                        left join (select sr.uv_id, count(1) as cant_vif
                        from seguridad_requerimiento sr
                        left join seguridad_delito sd
                            on sd.id = sr.delito_id
                        where sd.clasificacion_delito_id = 2
                        group by sr.uv_id) vif
                            on cu.id = vif.uv_id
                        left join (select sr.uv_id, count(1) as cant_inc
                        from seguridad_requerimiento sr
                        left join seguridad_delito sd
                            on sd.id = sr.delito_id
                        where sd.clasificacion_delito_id = 3
                        group by sr.uv_id) inc
                            on cu.id = inc.uv_id
                        left join (select sr.uv_id, count(1) as cant_asx
                        from seguridad_requerimiento sr
                        left join seguridad_delito sd
                            on sd.id = sr.delito_id
                        where sd.clasificacion_delito_id = 4
                        group by sr.uv_id) asx
                            on cu.id = asx.uv_id
                        left join (select sr.uv_id, count(1) as cant_ai
                        from seguridad_requerimiento sr
                        left join seguridad_delito sd
                            on sd.id = sr.delito_id
                        where sd.clasificacion_delito_id = 5
                        group by sr.uv_id) ai
                            on cu.id = ai.uv_id
                        left join (select sr.uv_id, count(1) as cant_der
                        from seguridad_requerimiento sr
                        left join seguridad_delito sd
                            on sd.id = sr.delito_id
                        where sd.clasificacion_delito_id = 6
                        group by sr.uv_id) der
                            on cu.id = der.uv_id
                        left join (select sr.uv_id, count(1) as cant_otro
                        from seguridad_requerimiento sr
                        left join seguridad_delito sd
                            on sd.id = sr.delito_id
                        where sd.clasificacion_delito_id = 7
                        group by sr.uv_id) otro
                            on cu.id = otro.uv_id'''

        for c in Delito.objects.raw(query_tabla):
            diccionario_tabla[c.id] = [c.total, c.delito, c.vif, c.inc, c.asx, c.ai, c.der, c.otro]
        
        #FILTRO POR CATEGORIA 

        if filtro_mapa[categoria] == "Total":

            lista_mapa_total = []
            query_mapa = '''select cu.numero_uv as id, sr.created
                            from seguridad_requerimiento sr 
                            left join core_uv cu
                                on sr.uv_id = cu.id
                            where sr.uv_id <> 0
                            order by sr.created asc'''
            
            for c in Requerimiento.objects.raw(query_mapa):
                lista_mapa_total.append({"uv":c.id,"created": str(c.created)})
                
            lista_mapa = lista_mapa_total

        elif filtro_mapa[categoria] == "Delito de mayor connotacion social":
            lista_mapa_delito = []
            query_mapa = '''select cu.numero_uv as id, sr.created
                            from seguridad_requerimiento sr 
                            left join core_uv cu
                                on sr.uv_id = cu.id
                            left join seguridad_delito sd
                                on sr.delito_id =  sd.id
                            where sr.uv_id <> 0
                            and sd.clasificacion_delito_id = 1
                            order by sr.created asc'''
            
            for c in Requerimiento.objects.raw(query_mapa):
                lista_mapa_delito.append({"uv":c.id,"created": str(c.created)})
                
            lista_mapa = lista_mapa_delito

        elif filtro_mapa[categoria] == "Violencia Intrafamiliar":
            lista_mapa_vif = []
            query_mapa = '''select cu.numero_uv as id, sr.created
                            from seguridad_requerimiento sr 
                            left join core_uv cu
                                on sr.uv_id = cu.id
                            left join seguridad_delito sd
                                on sr.delito_id =  sd.id
                            where sr.uv_id <> 0
                            and sd.clasificacion_delito_id = 2
                            order by sr.created asc'''
            
            for c in Requerimiento.objects.raw(query_mapa):
                lista_mapa_vif.append({"uv":c.id,"created": str(c.created)})
                
            lista_mapa = lista_mapa_vif
            
        elif filtro_mapa[categoria] == "Incivilidades":
            lista_mapa_inc = []
            query_mapa = '''select cu.numero_uv as id, sr.created
                            from seguridad_requerimiento sr 
                            left join core_uv cu
                                on sr.uv_id = cu.id
                            left join seguridad_delito sd
                                on sr.delito_id =  sd.id
                            where sr.uv_id <> 0
                            and sd.clasificacion_delito_id = 3
                            order by sr.created asc'''
            
            for c in Requerimiento.objects.raw(query_mapa):
                lista_mapa_inc.append({"uv":c.id,"created": str(c.created)})
                
            lista_mapa = lista_mapa_inc

        elif filtro_mapa[categoria] == "Abusos sexuales":
            lista_mapa_asx = []
            query_mapa = '''select cu.numero_uv as id, sr.created
                            from seguridad_requerimiento sr 
                            left join core_uv cu
                                on sr.uv_id = cu.id
                            left join seguridad_delito sd
                                on sr.delito_id =  sd.id
                            where sr.uv_id <> 0
                            and sd.clasificacion_delito_id = 4
                            order by sr.created asc'''
            
            for c in Requerimiento.objects.raw(query_mapa):
                lista_mapa_asx.append({"uv":c.id,"created": str(c.created)})
                
            lista_mapa = lista_mapa_asx

        elif filtro_mapa[categoria] == "Accidentes e incendios":
            lista_mapa_ai = []
            query_mapa = '''select cu.numero_uv as id, sr.created
                            from seguridad_requerimiento sr 
                            left join core_uv cu
                                on sr.uv_id = cu.id
                            left join seguridad_delito sd
                                on sr.delito_id =  sd.id
                            where sr.uv_id <> 0
                            and sd.clasificacion_delito_id = 5
                            order by sr.created asc'''
            
            for c in Requerimiento.objects.raw(query_mapa):
                lista_mapa_ai.append({"uv":c.id,"created": str(c.created)})
                
            lista_mapa = lista_mapa_ai

        elif filtro_mapa[categoria] == "Derivaciones":
            lista_mapa_der = []
            query_mapa = '''select cu.numero_uv as id, sr.created
                            from seguridad_requerimiento sr 
                            left join core_uv cu
                                on sr.uv_id = cu.id
                            left join seguridad_delito sd
                                on sr.delito_id =  sd.id
                            where sr.uv_id <> 0
                            and sd.clasificacion_delito_id = 6
                            order by sr.created asc'''
            
            for c in Requerimiento.objects.raw(query_mapa):
                lista_mapa_der.append({"uv":c.id,"created": str(c.created)})
                
            lista_mapa = lista_mapa_der

        elif filtro_mapa[categoria] == "Otro":
            lista_mapa_otro = []
            query_mapa = '''select cu.numero_uv as id, sr.created
                            from seguridad_requerimiento sr 
                            left join core_uv cu
                                on sr.uv_id = cu.id
                            left join seguridad_delito sd
                                on sr.delito_id =  sd.id
                            where sr.uv_id <> 0
                            and sd.clasificacion_delito_id = 7
                            order by sr.created asc'''
            
            for c in Requerimiento.objects.raw(query_mapa):
                lista_mapa_otro.append({"uv":c.id,"created": str(c.created)})
                
            lista_mapa = lista_mapa_otro
       
        context = {
            'filtro_tiempo':filtro_tiempo,
            'lista_mapa': lista_mapa,
            'diccionario_tabla': diccionario_tabla,
        }

        return render(request,'vis/seguridad_vis.html', context)

    if request.method == 'POST':
        filtro_tiempo=FiltroTiempo(request.POST)
        
        if filtro_tiempo.is_valid():
            fecha_inicio = filtro_tiempo.cleaned_data.get('fecha_inicio')
            fecha_fin = filtro_tiempo.cleaned_data.get('fecha_fin')

            # diccionario_tabla = {}
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
            #     diccionario_tabla[c.id] = [
            #         c.total,
            #         c.delito,
            #         c.vif,
            #         c.inc,
            #         c.asx,
            #         c.ai,
            #         c.der,
            #         c.otro,
            #     ]

            #FILTRO POR CATEGORIA 

            if filtro_mapa[categoria] == "Total":

                lista_mapa_total = []
                query_mapa = f"select cu.numero_uv as id, sr.created \
                                from seguridad_requerimiento sr \
                                left join core_uv cu \
                                    on sr.uv_id = cu.id \
                                where sr.uv_id <> 0 \
                                and sr.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by sr.created asc"
                
                for c in Requerimiento.objects.raw(query_mapa):
                    lista_mapa_total.append({"uv":c.uv.numero_uv,"created": str(c.created)})
                    
                lista_mapa = lista_mapa_total

    #         elif filtro_mapa[categoria] == "Delito de mayor connotacion social":
    #             lista_mapa_delito = []
    #             query_mapa = '''select dc.id, cu.numero_uv as uc, dc.created
    #                             from dimap_controlplaga dc
    #                             left join core_persona cp 
    #                                 on dc.persona_id = cp.id
    #                             left join core_uv cu
    #                                 on cp.uv_id = cu.id
    #                             where cu.numero_uv <> 0
    #                             order by dc.created asc;'''
                
    #             for c in Requerimiento.objects.raw(query_mapa):
    #                 lista_mapa_delito.append({"uv":c.uv.numero_uv,"created": str(c.created)})
                    
    #             lista_mapa = lista_mapa_delito

    #         elif filtro_mapa[categoria] == "Violencia Intrafamiliar":
    #             lista_mapa_vif = []
    #             query_mapa = '''select dc.id, cu.numero_uv as uc, dc.created
    #                             from dimap_controlplaga dc
    #                             left join core_persona cp 
    #                                 on dc.persona_id = cp.id
    #                             left join core_uv cu
    #                                 on cp.uv_id = cu.id
    #                             where cu.numero_uv <> 0
    #                             order by dc.created asc;'''
                
    #             for c in Requerimiento.objects.raw(query_mapa):
    #                 lista_mapa_vif.append({"uv":c.uv.numero_uv,"created": str(c.created)})
                    
    #             lista_mapa = lista_mapa_vif
                
    #         elif filtro_mapa[categoria] == "Incivilidades":
    #             lista_mapa_inc = []
    #             query_mapa = '''select dc.id, cu.numero_uv as uc, dc.created
    #                             from dimap_controlplaga dc
    #                             left join core_persona cp 
    #                                 on dc.persona_id = cp.id
    #                             left join core_uv cu
    #                                 on cp.uv_id = cu.id
    #                             where cu.numero_uv <> 0
    #                             order by dc.created asc;'''
                
    #             for c in Requerimiento.objects.raw(query_mapa):
    #                 lista_mapa_inc.append({"uv":c.uv.numero_uv,"created": str(c.created)})
                    
    #             lista_mapa = lista_mapa_inc

    #         elif filtro_mapa[categoria] == "Abusos sexuales":
    #             lista_mapa_asx = []
    #             query_mapa = '''select dc.id, cu.numero_uv as uc, dc.created
    #                             from dimap_controlplaga dc
    #                             left join core_persona cp 
    #                                 on dc.persona_id = cp.id
    #                             left join core_uv cu
    #                                 on cp.uv_id = cu.id
    #                             where cu.numero_uv <> 0
    #                             order by dc.created asc;'''
                
    #             for c in Requerimiento.objects.raw(query_mapa):
    #                 lista_mapa_asx.append({"uv":c.uv.numero_uv,"created": str(c.created)})
                    
    #             lista_mapa = lista_mapa_asx

    #         elif filtro_mapa[categoria] == "Accidentes e incendios":
    #             lista_mapa_ai = []
    #             query_mapa = '''select dc.id, cu.numero_uv as uc, dc.created
    #                             from dimap_controlplaga dc
    #                             left join core_persona cp 
    #                                 on dc.persona_id = cp.id
    #                             left join core_uv cu
    #                                 on cp.uv_id = cu.id
    #                             where cu.numero_uv <> 0
    #                             order by dc.created asc;'''
                
    #             for c in Requerimiento.objects.raw(query_mapa):
    #                 lista_mapa_ai.append({"uv":c.uv.numero_uv,"created": str(c.created)})
                    
    #             lista_mapa = lista_mapa_ai

    #         elif filtro_mapa[categoria] == "Derivaciones":
    #             lista_mapa_der = []
    #             query_mapa = '''select dc.id, cu.numero_uv as uc, dc.created
    #                             from dimap_controlplaga dc
    #                             left join core_persona cp 
    #                                 on dc.persona_id = cp.id
    #                             left join core_uv cu
    #                                 on cp.uv_id = cu.id
    #                             where cu.numero_uv <> 0
    #                             order by dc.created asc;'''
                
    #             for c in Requerimiento.objects.raw(query_mapa):
    #                 lista_mapa_der.append({"uv":c.uv.numero_uv,"created": str(c.created)})
                    
    #             lista_mapa = lista_mapa_der

    #         elif filtro_mapa[categoria] == "Otro":
    #             lista_mapa_otro = []
    #             query_mapa = '''select dc.id, cu.numero_uv as uc, dc.created
    #                             from dimap_controlplaga dc
    #                             left join core_persona cp 
    #                                 on dc.persona_id = cp.id
    #                             left join core_uv cu
    #                                 on cp.uv_id = cu.id
    #                             where cu.numero_uv <> 0
    #                             order by dc.created asc;'''
                
    #             for c in Requerimiento.objects.raw(query_mapa):
    #                 lista_mapa_otro.append({"uv":c.uv.numero_uv,"created": str(c.created)})
                    
    #             lista_mapa = lista_mapa_otro
        
            context = {
                'filtro_tiempo':filtro_tiempo,
                'lista_mapa': lista_mapa,
                # 'diccionario_tabla': diccionario_tabla,
            }

            return render(request,'vis/seguridad_vis.html', context)

    