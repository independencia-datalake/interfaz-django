from django.shortcuts import render, redirect
from .forms import(FiltroTiempo)
from farmacia.models import(ComprobanteVenta)
from datetime import datetime
from dimap.models import(
    ControlPlaga,
    Procedimiento,
    SeguridadDIMAP
)
from seguridad.models import(
    Requerimiento, 
    Delito, 
    ClasificacionDelito
)
from carga.models import(
    EntregasPandemia,
    LicenciaConducir,
    PermisosCirculacion,
    Empresas,
    ExencionAseo,
    DOM
)


def inicio_vis(request):
    filtro_tiempo=FiltroTiempo(request.POST or None)

    lista_mapa = [{'uv': 0, 'created': '2022-03-13 15:20:40.167757'}]
    diccionario_tabla = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0}



    context = {
        'filtro_tiempo':filtro_tiempo,
        'lista_mapa':lista_mapa,
        'diccionario_tabla': diccionario_tabla
    }


    return render(request, 'vis/home_vis.html', context)

#FARMACIA (LISTO)
def farmacia_vis(request):
    if request.method == 'GET':

        diccionario_tabla = {}
        query_tabla = '''select cu.numero_uv as id, 
                        coalesce(f.cant, 0) as cant
                        from core_uv cu
                        left join (select cu.numero_uv as uv, count(1) as cant
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


        tiempo = []
        query_tiempo = '''select 1 as id, max(fc.created) max, min(fc.created) min
                        from (select u.id, u.numero_uv, fc.created ,max(fc.created) max, min(fc.created) min
                        from farmacia_comprobanteventa fc
                        left join core_persona p
                            on fc.comprador_id = p.id
                        left join core_uv u
                            on p.uv_id = u.id 
                        GROUP BY u.id, fc.created) as fc'''

        for c in ComprobanteVenta.objects.raw(query_tiempo):
            tiempo = {"max":c.max,"min": c.min}


        #fecha_inicio = datetime.strptime(tiempo['min'], '%Y-%m-%d %H:%M:%S.%f')
        #fecha_fin = datetime.strptime(tiempo['max'], '%Y-%m-%d %H:%M:%S.%f')

        fecha_inicio = datetime.strftime(tiempo['min'], '%Y-%m-%d')
        fecha_fin = datetime.strftime(tiempo['max'], '%Y-%m-%d')

        fechas_categoria = {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'categoria': 'farmacia'
        }
        
        filtro_tiempo=FiltroTiempo(fechas_categoria or None)

        context = {
            'filtro_tiempo':filtro_tiempo,
            'lista_mapa':lista_mapa,
            'diccionario_tabla': diccionario_tabla,
            'fechas_categoria': fechas_categoria
        }

        return render(request,'vis/farmacia_vis.html', context)

    if request.method == 'POST':

        filtro_tiempo=FiltroTiempo(request.POST)
        if filtro_tiempo.is_valid():
            fecha_inicio = filtro_tiempo.cleaned_data.get('fecha_inicio')
            fecha_fin = filtro_tiempo.cleaned_data.get('fecha_fin')
            
            diccionario_tabla = {}
            query_tabla = f"select cu.numero_uv as id, \
                            coalesce(f.cant, 0) as cant \
                            from core_uv cu \
                            left join (select cu.numero_uv as uv, count(1) as cant \
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


            fechas_categoria = {
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'categoria': 'farmacia'
            }

            context = {
                'filtro_tiempo':filtro_tiempo,
                'diccionario_tabla': diccionario_tabla,
                'lista_mapa': lista_mapa,
                'fechas_categoria': fechas_categoria
            }
            
            return render(request,'vis/farmacia_vis.html', context)

#DIMAP HIGIENE (LISTO)
def dimap_vis(request,categoria):
    filtro_mapa = [
        "total",
        "esterilizacion",
        "denuncia",
        "control de plaga"
    ]

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
                            union all
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
                            union all
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

        
        
        tiempo = []
        query_tiempo = '''select 1 as id, max(a.created) max, min(a.created) min 
                            from (select a.uc as id, a.created
							from(select cu.numero_uv as uc, dc.created
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
                            GROUP BY a.created, a.uc
                            order by a.created) as a'''

        
        for c in SeguridadDIMAP.objects.raw(query_tiempo):
            tiempo = {"max":c.max,"min": c.min}

        fecha_inicio = datetime.strftime(tiempo['min'], '%Y-%m-%d')
        fecha_fin = datetime.strftime(tiempo['max'], '%Y-%m-%d')

        

        fechas_categoria = {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'categoria': filtro_mapa[categoria]
        }

        filtro_tiempo=FiltroTiempo(fechas_categoria or None)
        
        context = {
            'filtro_tiempo':filtro_tiempo,
            'lista_mapa': lista_mapa,
            'diccionario_tabla': diccionario_tabla,
            'fechas_categoria': fechas_categoria
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

            fechas_categoria = {
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'categoria': filtro_mapa[categoria]
            }

            context = {
                'filtro_tiempo':filtro_tiempo,
                'lista_mapa': lista_mapa,
                'diccionario_tabla': diccionario_tabla,
                'fechas_categoria':fechas_categoria
            }

            return render(request,'vis/dimap_vis.html', context)

#SEGURIDAD MUNICIPAL (LISTO)
def seguridad_vis(request, categoria):
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
            diccionario_tabla[c.id] = [
                c.total,
                c.delito,
                c.vif,
                c.inc,
                c.asx,
                c.ai,
                c.der,
                c.otro
            ]
        
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
       
        tiempo = []
        query_tiempo = '''select cu.numero_uv as id, sr.created, max(sr.created) max, min(sr.created) min
                            from seguridad_requerimiento sr 
                            left join core_uv cu
                                on sr.uv_id = cu.id
                            where sr.uv_id <> 0
                            GROUP BY cu.id, sr.created;'''

                            #order by sr.created asc'''

        query_tiempo_date = '''select 1 as id, max(sr.created) max, min(sr.created) min
                            from (select cu.numero_uv as id, sr.created, max(sr.created) max, min(sr.created) min
                            from seguridad_requerimiento sr 
                            left join core_uv cu
                                on sr.uv_id = cu.id
                            where sr.uv_id <> 0
                            GROUP BY cu.id, sr.created
                            order by sr.created asc) as sr'''
        for c in Requerimiento.objects.raw(query_tiempo_date): 
            tiempo = {"max":c.max,"min": c.min}
        # for c in Requerimiento.objects.raw(query_tiempo): #!todo OJO ACA // MODEL EXTRAÑO
        #     tiempo = {"max":c.max,"min": c.min}

        fecha_inicio = datetime.strftime(tiempo['min'], '%Y-%m-%d')
        fecha_fin = datetime.strftime(tiempo['max'], '%Y-%m-%d')
       

        fechas_categoria = {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'categoria': filtro_mapa[categoria]
        }

        filtro_tiempo=FiltroTiempo(fechas_categoria or None)

        context = {
            'filtro_tiempo':filtro_tiempo,
            'lista_mapa': lista_mapa,
            'diccionario_tabla': diccionario_tabla,
            'fechas_categoria': fechas_categoria
        }

        return render(request,'vis/seguridad_vis.html', context)

    if request.method == 'POST':
        filtro_tiempo=FiltroTiempo(request.POST)
        
        if filtro_tiempo.is_valid():
            fecha_inicio = filtro_tiempo.cleaned_data.get('fecha_inicio')
            fecha_fin = filtro_tiempo.cleaned_data.get('fecha_fin')

            diccionario_tabla = {}
            query_tabla = f"select cu.numero_uv as id, \
                            coalesce(dm.cant_delito, 0) + coalesce(vif.cant_vif, 0) + coalesce(inc.cant_inc, 0) + coalesce(asx.cant_asx, 0) + coalesce(ai.cant_ai, 0) + coalesce(der.cant_der, 0) + coalesce(otro.cant_otro, 0) total, \
                            case when dm.cant_delito is null then 0 else dm.cant_delito end delito, \
                            case when vif.cant_vif is null then 0 else vif.cant_vif end vif, \
                            case when inc.cant_inc is null then 0 else inc.cant_inc end inc, \
                            case when asx.cant_asx is null then 0 else asx.cant_asx end asx, \
                            case when ai.cant_ai is null then 0 else ai.cant_ai end ai, \
                            case when der.cant_der is null then 0 else der.cant_der end der, \
                            case when otro.cant_otro is null then 0 else otro.cant_otro end otro \
                            from core_uv cu \
                            left join (select sr.uv_id, count(1) as cant_delito \
                            from seguridad_requerimiento sr \
                            left join seguridad_delito sd \
                                on sd.id = sr.delito_id \
                            where sd.clasificacion_delito_id = 1 \
                            and sr.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            group by sr.uv_id) dm \
                                on cu.id = dm.uv_id \
                            left join (select sr.uv_id, count(1) as cant_vif \
                            from seguridad_requerimiento sr \
                            left join seguridad_delito sd \
                                on sd.id = sr.delito_id \
                            where sd.clasificacion_delito_id = 2 \
                            and sr.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            group by sr.uv_id) vif \
                                on cu.id = vif.uv_id \
                            left join (select sr.uv_id, count(1) as cant_inc \
                            from seguridad_requerimiento sr \
                            left join seguridad_delito sd \
                                on sd.id = sr.delito_id \
                            where sd.clasificacion_delito_id = 3 \
                            and sr.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            group by sr.uv_id) inc \
                                on cu.id = inc.uv_id \
                            left join (select sr.uv_id, count(1) as cant_asx \
                            from seguridad_requerimiento sr \
                            left join seguridad_delito sd \
                                on sd.id = sr.delito_id \
                            where sd.clasificacion_delito_id = 4 \
                            and sr.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            group by sr.uv_id) asx \
                                on cu.id = asx.uv_id \
                            left join (select sr.uv_id, count(1) as cant_ai \
                            from seguridad_requerimiento sr \
                            left join seguridad_delito sd \
                                on sd.id = sr.delito_id \
                            where sd.clasificacion_delito_id = 5 \
                            and sr.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            group by sr.uv_id) ai \
                                on cu.id = ai.uv_id \
                            left join (select sr.uv_id, count(1) as cant_der \
                            from seguridad_requerimiento sr \
                            left join seguridad_delito sd \
                                on sd.id = sr.delito_id \
                            where sd.clasificacion_delito_id = 6 \
                            and sr.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            group by sr.uv_id) der \
                                on cu.id = der.uv_id \
                            left join (select sr.uv_id, count(1) as cant_otro \
                            from seguridad_requerimiento sr \
                            left join seguridad_delito sd \
                                on sd.id = sr.delito_id \
                            where sd.clasificacion_delito_id = 7 \
                            and sr.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            group by sr.uv_id) otro \
                                on cu.id = otro.uv_id"

            for c in Delito.objects.raw(query_tabla):
                diccionario_tabla[c.id] = [
                    c.total,
                    c.delito,
                    c.vif,
                    c.inc,
                    c.asx,
                    c.ai,
                    c.der,
                    c.otro,
                ]

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
                    lista_mapa_total.append({"uv":c.id,"created": str(c.created)})
                    
                lista_mapa = lista_mapa_total

            elif filtro_mapa[categoria] == "Delito de mayor connotacion social":
                lista_mapa_delito = []
                query_mapa = f"select cu.numero_uv as id, sr.created \
                                from seguridad_requerimiento sr \
                                left join core_uv cu \
                                    on sr.uv_id = cu.id \
                                left join seguridad_delito sd \
                                    on sr.delito_id =  sd.id \
                                where sr.uv_id <> 0 \
                                and sd.clasificacion_delito_id = 1 \
                                and sr.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by sr.created asc"
                
                for c in Requerimiento.objects.raw(query_mapa):
                    lista_mapa_delito.append({"uv":c.uv.numero_uv,"created": str(c.created)})
                    
                lista_mapa = lista_mapa_delito

            elif filtro_mapa[categoria] == "Violencia Intrafamiliar":
                lista_mapa_vif = []
                query_mapa = f"select cu.numero_uv as id, sr.created \
                                from seguridad_requerimiento sr \
                                left join core_uv cu \
                                    on sr.uv_id = cu.id \
                                left join seguridad_delito sd \
                                    on sr.delito_id =  sd.id \
                                where sr.uv_id <> 0 \
                                and sd.clasificacion_delito_id = 2 \
                                and sr.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by sr.created asc" 
                
                for c in Requerimiento.objects.raw(query_mapa):
                    lista_mapa_vif.append({"uv":c.id,"created": str(c.created)})
                    
                lista_mapa = lista_mapa_vif
                
            elif filtro_mapa[categoria] == "Incivilidades":
                lista_mapa_inc = []
                query_mapa = f"select cu.numero_uv as id, sr.created \
                                from seguridad_requerimiento sr \
                                left join core_uv cu \
                                    on sr.uv_id = cu.id \
                                left join seguridad_delito sd \
                                    on sr.delito_id =  sd.id \
                                where sr.uv_id <> 0 \
                                and sd.clasificacion_delito_id = 3 \
                                and sr.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by sr.created asc"
                
                for c in Requerimiento.objects.raw(query_mapa):
                    lista_mapa_inc.append({"uv":c.id,"created": str(c.created)})
                    
                lista_mapa = lista_mapa_inc

            elif filtro_mapa[categoria] == "Abusos sexuales":
                lista_mapa_asx = []
                query_mapa = f"select cu.numero_uv as id, sr.created \
                                from seguridad_requerimiento sr \
                                left join core_uv cu \
                                    on sr.uv_id = cu.id \
                                left join seguridad_delito sd \
                                    on sr.delito_id =  sd.id \
                                where sr.uv_id <> 0 \
                                and sd.clasificacion_delito_id = 4 \
                                and sr.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by sr.created asc"
                
                for c in Requerimiento.objects.raw(query_mapa):
                    lista_mapa_asx.append({"uv":c.id,"created": str(c.created)})
                    
                lista_mapa = lista_mapa_asx

            elif filtro_mapa[categoria] == "Accidentes e incendios":
                lista_mapa_ai = []
                query_mapa = f"select cu.numero_uv as id, sr.created \
                            from seguridad_requerimiento sr \
                            left join core_uv cu \
                                on sr.uv_id = cu.id \
                            left join seguridad_delito sd \
                                on sr.delito_id =  sd.id \
                            where sr.uv_id <> 0 \
                            and sd.clasificacion_delito_id = 5 \
                            and sr.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            order by sr.created asc"
                
                for c in Requerimiento.objects.raw(query_mapa):
                    lista_mapa_ai.append({"uv":c.id,"created": str(c.created)})
                    
                lista_mapa = lista_mapa_ai

            elif filtro_mapa[categoria] == "Derivaciones":
                lista_mapa_der = []
                query_mapa = f"select cu.numero_uv as id, sr.created \
                            from seguridad_requerimiento sr \
                            left join core_uv cu \
                                on sr.uv_id = cu.id \
                            left join seguridad_delito sd \
                                on sr.delito_id =  sd.id \
                            where sr.uv_id <> 0 \
                            and sd.clasificacion_delito_id = 6 \
                            and sr.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            order by sr.created asc"
                
                for c in Requerimiento.objects.raw(query_mapa):
                    lista_mapa_der.append({"uv":c.id,"created": str(c.created)})
                    
                lista_mapa = lista_mapa_der

            elif filtro_mapa[categoria] == "Otro":
                lista_mapa_otro = []
                query_mapa = f"select cu.numero_uv as id, sr.created \
                            from seguridad_requerimiento sr \
                            left join core_uv cu \
                                on sr.uv_id = cu.id \
                            left join seguridad_delito sd \
                                on sr.delito_id =  sd.id \
                            where sr.uv_id <> 0 \
                            and sd.clasificacion_delito_id = 7 \
                            and sr.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            order by sr.created asc"
                
                for c in Requerimiento.objects.raw(query_mapa):
                    lista_mapa_otro.append({"uv":c.id,"created": str(c.created)})
                    
                lista_mapa = lista_mapa_otro
        
            fechas_categoria = {
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'categoria': filtro_mapa[categoria]
            }

            context = {
                'filtro_tiempo':filtro_tiempo,
                'lista_mapa': lista_mapa,
                'diccionario_tabla': diccionario_tabla,
                'fechas_categoria':fechas_categoria
            }

            return render(request,'vis/seguridad_vis.html', context)

#EXENCION DE BASURA (LISTO)
def exencion_vis(request, categoria):
    filtro_mapa = [
        "Total",
        "50% de Excencion",
        "75% de Excencion",
        "100% de Excencion",
    ]

    if request.method == 'GET':

        diccionario_tabla = {}
        query_tabla = '''select cu.numero_uv as id,
                            coalesce(ex50.cant, 0) + coalesce(ex75.cant, 0) + coalesce(ex1.cant, 0) as total,
                            case when ex50.cant is null then 0 else ex50.cant end ex50,
                            case when ex75.cant is null then 0 else ex75.cant end ex75,
                            case when ex1.cant is null then 0 else ex1.cant end ex1
                        from core_uv cu
                        left join (
                            select ce.uv_id as uv, count(1) as cant
                            from carga_exencionaseo ce
                            where ce.porcentaje_exencion = 0.5
                            group by ce.uv_id) ex50
                            on cu.id = ex50.uv
                        left join (
                            select ce.uv_id as uv, count(1) as cant
                            from carga_exencionaseo ce
                            where ce.porcentaje_exencion = 0.75
                            group by ce.uv_id) ex75
                            on cu.id = ex75.uv
                        left join (
                            select ce.uv_id as uv, count(1) as cant
                            from carga_exencionaseo ce
                            where ce.porcentaje_exencion = 1
                            group by ce.uv_id) ex1
                            on cu.id = ex1.uv'''

        for c in ExencionAseo.objects.raw(query_tabla):
            diccionario_tabla[c.id] = [
                c.total,
                c.ex50,
                c.ex75,
                c.ex1
            ]
        


        #FILTRO POR CATEGORIA 

        if filtro_mapa[categoria] == "Total":

            lista_mapa_total = []
            query_mapa = '''select ce.uv_id as id,
                                ce.marca_temporal
                            from carga_exencionaseo ce
                            where ce.uv_id <> 0
                            order by ce.marca_temporal asc;'''
            
            for c in ExencionAseo.objects.raw(query_mapa):
                lista_mapa_total.append({"uv":c.id-1,"created": str(c.marca_temporal)})
                
            lista_mapa = lista_mapa_total

        elif filtro_mapa[categoria] == "50% de Excencion":
            
            lista_mapa_50 = []
            query_mapa = '''select ce.uv_id as id, ce.marca_temporal
                            from carga_exencionaseo ce
                            where ce.uv_id <> 0
                            and ce.porcentaje_exencion = 0.5
                            order by ce.marca_temporal asc;'''
            
            for c in ExencionAseo.objects.raw(query_mapa):
                lista_mapa_50.append({"uv":c.id-1,"created": str(c.marca_temporal)})
                
            lista_mapa = lista_mapa_50

        elif filtro_mapa[categoria] == "75% de Excencion":

            lista_mapa_75 = []
            query_mapa = '''select ce.uv_id as id, ce.marca_temporal
                            from carga_exencionaseo ce
                            where ce.uv_id <> 0
                            and ce.porcentaje_exencion = 0.75
                            order by ce.marca_temporal asc;'''
            
            for c in ExencionAseo.objects.raw(query_mapa):
                lista_mapa_75.append({"uv":c.id-1,"created": str(c.marca_temporal)})
                
            lista_mapa = lista_mapa_75

        elif filtro_mapa[categoria] == "100% de Excencion":

            lista_mapa_1 = []
            query_mapa = '''select ce.uv_id as id, ce.marca_temporal
                            from carga_exencionaseo ce
                            where ce.uv_id <> 0
                            and ce.porcentaje_exencion = 1
                            order by ce.marca_temporal asc;'''
            
            for c in ExencionAseo.objects.raw(query_mapa):
                lista_mapa_1.append({"uv":c.id-1,"created": str(c.marca_temporal)})
                
            lista_mapa = lista_mapa_1

        tiempo = []
        query_tiempo = '''select 1 as id, max(ce.marca_temporal) max, min(ce.marca_temporal) min
                            from (select ce.uv_id as id, ce.marca_temporal
                            from carga_exencionaseo ce
                            where ce.uv_id <> 0
                            GROUP BY ce.uv_id, marca_temporal  
                            order by ce.marca_temporal asc) as ce''' #todo SE AGREGO GROUP BY

        for c in ExencionAseo.objects.raw(query_tiempo):
            tiempo = {"max":c.max,"min": c.min}

        fecha_inicio = datetime.strftime(tiempo['min'], '%Y-%m-%d')
        fecha_fin = datetime.strftime(tiempo['max'], '%Y-%m-%d')

        fechas_categoria = {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'categoria': filtro_mapa[categoria]
        }

        filtro_tiempo=FiltroTiempo(fechas_categoria or None)


        context = {
            'filtro_tiempo':filtro_tiempo,
            'lista_mapa': lista_mapa,
            'diccionario_tabla': diccionario_tabla,
            'fechas_categoria': fechas_categoria
        }

        return render(request,'vis/exencion_basura_vis.html',context)

    if request.method == 'POST':
        filtro_tiempo=FiltroTiempo(request.POST)

        if filtro_tiempo.is_valid():
            fecha_inicio = filtro_tiempo.cleaned_data.get('fecha_inicio')
            fecha_fin = filtro_tiempo.cleaned_data.get('fecha_fin')

            diccionario_tabla = {}
            query_tabla = f"select cu.numero_uv as id, \
                                coalesce(ex50.cant, 0) + coalesce(ex75.cant, 0) + coalesce(ex1.cant, 0) as total, \
                                case when ex50.cant is null then 0 else ex50.cant end ex50, \
                                case when ex75.cant is null then 0 else ex75.cant end ex75, \
                                case when ex1.cant is null then 0 else ex1.cant end ex1 \
                            from core_uv cu \
                            left join ( \
                                select ce.uv_id as uv, count(1) as cant \
                                from carga_exencionaseo ce \
                                where ce.porcentaje_exencion = 0.5 \
                                and ce.marca_temporal between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by ce.uv_id) ex50 \
                                on cu.id = ex50.uv \
                            left join ( \
                                select ce.uv_id as uv, count(1) as cant \
                                from carga_exencionaseo ce \
                                where ce.porcentaje_exencion = 0.75 \
                                and ce.marca_temporal between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by ce.uv_id) ex75 \
                                on cu.id = ex75.uv \
                            left join ( \
                                select ce.uv_id as uv, count(1) as cant \
                                from carga_exencionaseo ce \
                                where ce.porcentaje_exencion = 1 \
                                and ce.marca_temporal between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by ce.uv_id) ex1 \
                                on cu.id = ex1.uv"

            for c in ExencionAseo.objects.raw(query_tabla):
                        diccionario_tabla[c.id] = [
                            c.total,
                            c.ex50,
                            c.ex75,
                            c.ex1
                        ]

            #FILTRO POR CATEGORIA 

            if filtro_mapa[categoria] == "Total":

                lista_mapa_total = []
                query_mapa = f"select ce.uv_id as id, \
                                    ce.marca_temporal \
                                from carga_exencionaseo ce \
                                where ce.uv_id <> 0 \
                                and ce.marca_temporal between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by ce.marca_temporal asc;"
                
                for c in ExencionAseo.objects.raw(query_mapa):
                    lista_mapa_total.append({"uv":c.id-1,"created": str(c.marca_temporal)})
                    
                lista_mapa = lista_mapa_total

            elif filtro_mapa[categoria] == "50% de Excencion":
                
                lista_mapa_50 = []
                query_mapa = f"select ce.uv_id as id, ce.marca_temporal \
                                from carga_exencionaseo ce \
                                where ce.uv_id <> 0 \
                                and ce.porcentaje_exencion = 0.5 \
                                and ce.marca_temporal between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by ce.marca_temporal asc;"
                
                for c in ExencionAseo.objects.raw(query_mapa):
                    lista_mapa_50.append({"uv":c.id-1,"created": str(c.marca_temporal)})
                    
                lista_mapa = lista_mapa_50

            elif filtro_mapa[categoria] == "75% de Excencion":

                lista_mapa_75 = []
                query_mapa = f"select ce.uv_id as id, ce.marca_temporal \
                                from carga_exencionaseo ce \
                                where ce.uv_id <> 0 \
                                and ce.porcentaje_exencion = 0.75 \
                                and ce.marca_temporal between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by ce.marca_temporal asc;"
                
                for c in ExencionAseo.objects.raw(query_mapa):
                    lista_mapa_75.append({"uv":c.id-1,"created": str(c.marca_temporal)})
                    
                lista_mapa = lista_mapa_75

            elif filtro_mapa[categoria] == "100% de Excencion":

                lista_mapa_1 = []
                query_mapa = f"select ce.uv_id as id, ce.marca_temporal \
                                from carga_exencionaseo ce \
                                where ce.uv_id <> 0 \
                                and ce.porcentaje_exencion = 1 \
                                and ce.marca_temporal between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by ce.marca_temporal asc;"
                
                for c in ExencionAseo.objects.raw(query_mapa):
                    lista_mapa_1.append({"uv":c.id-1,"created": str(c.marca_temporal)})
                    
                lista_mapa = lista_mapa_1
            
            fechas_categoria = {
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'categoria': filtro_mapa[categoria]
            }

            context = {
                'filtro_tiempo':filtro_tiempo,
                'lista_mapa': lista_mapa,
                'diccionario_tabla': diccionario_tabla,
                'fechas_categoria':fechas_categoria
            }

            return render(request,'vis/exencion_basura_vis.html',context)

#AYUDA EN PANDEMIA (LISTO)
def entrega_pandemia_vis(request, categoria):
    filtro_mapa = [
        "Total",
        "Caja",
        "Pañal niño",
        "Pañal adulto",
        "Leche",
        "NAT100",
        "Balon de Gas",
        "Parafina",
    ]

    if request.method == 'GET':

        diccionario_tabla = {}
        query_tabla = '''select cu.numero_uv as id,
                            coalesce(caja.cant, 0) + 
                            coalesce(nino.cant, 0) + 
                            coalesce(adulto.cant, 0) + 
                            coalesce(leche.cant, 0) +
                            coalesce(nat.cant, 0) +
                            coalesce(balon.cant, 0) +
                            coalesce(parafina.cant, 0)
                            as total,
                            case when caja.cant is null then 0 else caja.cant end caja,
                            case when nino.cant is null then 0 else nino.cant end nino,
                            case when adulto.cant is null then 0 else adulto.cant end adulto,
                            case when leche.cant is null then 0 else leche.cant end leche,
                            case when nat.cant is null then 0 else nat.cant end nat,
                            case when balon.cant is null then 0 else balon.cant end balon,
                            case when parafina.cant is null then 0 else parafina.cant end parafina
                        from core_uv cu
                        left join (
                            select uv_id as uv, count(1) as cant
                            from carga_entregaspandemia ce
                            where ce.caja_mercaderia is not null
                            group by ce.uv_id) caja
                            on cu.id = caja.uv
                        left join (
                            select ce.uv_id as uv, count(1) as cant
                            from carga_entregaspandemia ce
                            where ce.pañal_niño_m is not null
                            or ce.pañal_niño_g is not null
                            or ce.pañal_niño_xg is not null
                            or ce.pañal_niño_xxg is not null
                            group by ce.uv_id) nino
                            on cu.id = nino.uv
                        left join (
                            select ce.uv_id as uv, count(1) as cant
                            from carga_entregaspandemia ce
                            where ce.pañal_adulto is not null
                            group by ce.uv_id) adulto
                            on cu.id = adulto.uv
                        left join (
                            select ce.uv_id as uv, count(1) as cant
                            from carga_entregaspandemia ce
                            where ce.leche_entera is not null
                            or ce.leche_descremada is not null
                            group by ce.uv_id) leche
                            on cu.id = leche.uv
                        left join (
                            select ce.uv_id as uv, count(1) as cant
                            from carga_entregaspandemia ce
                            where ce.nat_100 is not null
                            group by ce.uv_id) nat
                            on cu.id = nat.uv
                        left join (
                            select ce.uv_id as uv, count(1) as cant
                            from carga_entregaspandemia ce
                            where ce.balon_gas is not null
                            group by ce.uv_id) balon
                            on cu.id = balon.uv
                        left join (
                            select ce.uv_id as uv, count(1) as cant
                            from carga_entregaspandemia ce
                            where ce.parafina is not null
                            group by ce.uv_id) parafina
                            on cu.id = parafina.uv'''

        for c in EntregasPandemia.objects.raw(query_tabla):
            diccionario_tabla[c.id] = [
                c.total,
                c.caja,
                c.nino,
                c.adulto,
                c.leche,
                c.nat,
                c.balon,
                c.parafina,
            ]
        
        #FILTRO POR CATEGORIA 

        if filtro_mapa[categoria] == "Total":

            lista_mapa_total = []
            query_mapa = '''select ce.uv_id as id,
                                ce.fecha
                            from carga_entregaspandemia ce 
                            where ce.uv_id <> 1
                            order by ce.fecha asc;'''
            
            for c in EntregasPandemia.objects.raw(query_mapa):
                lista_mapa_total.append({"uv":c.id-1,"created": str(c.fecha)})
                
            lista_mapa = lista_mapa_total

        elif filtro_mapa[categoria] == "Caja":

            lista_mapa_caja = []
            query_mapa = '''select ce.uv_id as id, ce.fecha
                            from carga_entregaspandemia ce
                            where ce.uv_id <> 1
                            and ce.caja_mercaderia is not null
                            order by ce.fecha asc;'''
            
            for c in EntregasPandemia.objects.raw(query_mapa):
                lista_mapa_caja.append({"uv":c.id-1,"created": str(c.fecha)})
                
            lista_mapa = lista_mapa_caja

        elif filtro_mapa[categoria] == "Pañal niño":

            lista_mapa_pañal_niño = []
            query_mapa = '''select ce.uv_id as id, ce.fecha
                            from carga_entregaspandemia ce
                            where ce.uv_id <> 1
                            and ce.pañal_niño_m is not null
                            or ce.pañal_niño_g is not null
                            or ce.pañal_niño_xg is not null
                            or ce.pañal_niño_xxg is not null
                            order by ce.fecha asc;'''
            
            for c in EntregasPandemia.objects.raw(query_mapa):
                lista_mapa_pañal_niño.append({"uv":c.id-1,"created": str(c.fecha)})
                
            lista_mapa = lista_mapa_pañal_niño

        elif filtro_mapa[categoria] == "Pañal adulto":

            lista_mapa_pañal_adulto = []
            query_mapa = '''select ce.uv_id as id, ce.fecha 
                            from carga_entregaspandemia ce
                            where ce.uv_id <> 1
                            and ce.pañal_adulto is not null
                            order by ce.fecha asc;'''
            
            for c in EntregasPandemia.objects.raw(query_mapa):
                lista_mapa_pañal_adulto.append({"uv":c.id-1,"created": str(c.fecha)})
                
            lista_mapa = lista_mapa_pañal_adulto

        elif filtro_mapa[categoria] == "Leche":

            lista_mapa_leche = []
            query_mapa = '''select ce.uv_id as id, ce.fecha 
                            from carga_entregaspandemia ce
                            where ce.uv_id <> 1
                            and ce.leche_entera is not null
                            or ce.leche_descremada is not null
                            order by ce.fecha asc;'''
            
            for c in EntregasPandemia.objects.raw(query_mapa):
                lista_mapa_leche.append({"uv":c.id-1,"created": str(c.fecha)})
                
            lista_mapa = lista_mapa_leche

        elif filtro_mapa[categoria] == "NAT100":

            lista_mapa_nat = []
            query_mapa = '''select ce.uv_id as id, ce.fecha 
                            from carga_entregaspandemia ce
                            where ce.uv_id <> 1
                            and ce.nat_100 is not null
                            order by ce.fecha asc;'''
            
            for c in EntregasPandemia.objects.raw(query_mapa):
                lista_mapa_nat.append({"uv":c.id-1,"created": str(c.fecha)})
                
            lista_mapa = lista_mapa_nat

        elif filtro_mapa[categoria] == "Balon de Gas":

            lista_mapa_balon = []
            query_mapa = '''select ce.uv_id as id, ce.fecha
                            from carga_entregaspandemia ce
                            where ce.uv_id <> 1
                            and ce.balon_gas is not null
                            order by ce.fecha asc;'''
            
            for c in EntregasPandemia.objects.raw(query_mapa):
                lista_mapa_balon.append({"uv":c.id-1,"created": str(c.fecha)})
                
            lista_mapa = lista_mapa_balon

        elif filtro_mapa[categoria] == "Parafina":

            lista_mapa_total = []
            query_mapa = '''select ce.uv_id as id, ce.fecha 
                            from carga_entregaspandemia ce
                            where ce.uv_id <> 1
                            and ce.parafina is not null
                            order by ce.fecha asc;'''
            
            for c in EntregasPandemia.objects.raw(query_mapa):
                lista_mapa_total.append({"uv":c.id-1,"created": str(c.fecha)})
                
            lista_mapa = lista_mapa_total
        


        tiempo = []
        query_tiempo = '''select 1 as id, max(ce.fecha) max, min(ce.fecha) min
                            from (select ce.uv_id as id, ce.fecha
                            from carga_entregaspandemia ce 
                            where ce.uv_id <> 1
                            order by ce.fecha asc) as ce''' #todo se agrego group by

        for c in EntregasPandemia.objects.raw(query_tiempo):
            tiempo = {"max":c.max,"min": c.min}

        fecha_inicio = datetime.strftime(tiempo['min'], '%Y-%m-%d')
        fecha_fin = datetime.strftime(tiempo['max'], '%Y-%m-%d')

        fechas_categoria = {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'categoria': filtro_mapa[categoria]
        }

        filtro_tiempo=FiltroTiempo(fechas_categoria or None)


        context = {
            'filtro_tiempo':filtro_tiempo,
            'lista_mapa': lista_mapa,
            'diccionario_tabla': diccionario_tabla,
            'fechas_categoria': fechas_categoria
        }

        return render(request,'vis/entrega_pandemia_vis.html', context)

    if request.method == 'POST':
        filtro_tiempo=FiltroTiempo(request.POST)

        if filtro_tiempo.is_valid():
            fecha_inicio = filtro_tiempo.cleaned_data.get('fecha_inicio')
            fecha_fin = filtro_tiempo.cleaned_data.get('fecha_fin')

            diccionario_tabla = {}
            query_tabla = f"select cu.numero_uv as id, \
                                coalesce(caja.cant, 0) + \
                                coalesce(nino.cant, 0) + \
                                coalesce(adulto.cant, 0) + \
                                coalesce(leche.cant, 0) + \
                                coalesce(nat.cant, 0) + \
                                coalesce(balon.cant, 0) + \
                                coalesce(parafina.cant, 0) \
                                as total, \
                                case when caja.cant is null then 0 else caja.cant end caja, \
                                case when nino.cant is null then 0 else nino.cant end nino, \
                                case when adulto.cant is null then 0 else adulto.cant end adulto, \
                                case when leche.cant is null then 0 else leche.cant end leche, \
                                case when nat.cant is null then 0 else nat.cant end nat, \
                                case when balon.cant is null then 0 else balon.cant end balon, \
                                case when parafina.cant is null then 0 else parafina.cant end parafina \
                            from core_uv cu \
                            left join ( \
                                select ce.uv_id as uv, count(1) as cant \
                                from carga_entregaspandemia ce \
                                where ce.caja_mercaderia is not null \
                                and ce.fecha between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by ce.uv_id) caja \
                                on cu.id = caja.uv \
                            left join ( \
                                select ce.uv_id as uv, count(1) as cant \
                                from carga_entregaspandemia ce \
                                where ce.pañal_niño_m is not null \
                                or ce.pañal_niño_g is not null \
                                or ce.pañal_niño_xg is not null \
                                or ce.pañal_niño_xxg is not null \
                                and ce.fecha between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by ce.uv_id) nino \
                                on cu.id = nino.uv \
                            left join ( \
                                select ce.uv_id as uv, count(1) as cant \
                                from carga_entregaspandemia ce \
                                where ce.pañal_adulto is not null \
                                and ce.fecha between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by ce.uv_id) adulto \
                                on cu.id = adulto.uv \
                            left join ( \
                                select ce.uv_id as uv, count(1) as cant \
                                from carga_entregaspandemia ce \
                                where ce.leche_entera is not null \
                                and ce.fecha between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                or ce.leche_descremada is not null \
                                group by ce.uv_id) leche \
                                on cu.id = leche.uv \
                            left join ( \
                                select ce.uv_id as uv, count(1) as cant \
                                from carga_entregaspandemia ce \
                                where ce.nat_100 is not null \
                                and ce.fecha between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by ce.uv_id) nat \
                                on cu.id = nat.uv \
                            left join ( \
                                select ce.uv_id as uv, count(1) as cant \
                                from carga_entregaspandemia ce \
                                where ce.balon_gas is not null \
                                and ce.fecha between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by ce.uv_id) balon \
                                on cu.id = balon.uv \
                            left join ( \
                                select ce.uv_id as uv, count(1) as cant \
                                from carga_entregaspandemia ce \
                                where ce.parafina is not null \
                                and ce.fecha between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by ce.uv_id) parafina \
                                on cu.id = parafina.uv"

            for c in EntregasPandemia.objects.raw(query_tabla):
                diccionario_tabla[c.id] = [
                    c.total,
                    c.caja,
                    c.nino,
                    c.adulto,
                    c.leche,
                    c.nat,
                    c.balon,
                    c.parafina,
                ]
            
            #FILTRO POR CATEGORIA 

            if filtro_mapa[categoria] == "Total":

                lista_mapa_total = []
                query_mapa = f"select ce.uv_id as id, \
                                    ce.fecha \
                                from carga_entregaspandemia ce \
                                where ce.uv_id <> 1 \
                                and ce.fecha between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by ce.fecha asc;"
                
                for c in EntregasPandemia.objects.raw(query_mapa):
                    lista_mapa_total.append({"uv":c.id-1,"created": str(c.fecha)})
                    
                lista_mapa = lista_mapa_total

            elif filtro_mapa[categoria] == "Caja":

                lista_mapa_caja = []
                query_mapa = f"select ce.uv_id as id, ce.fecha \
                                from carga_entregaspandemia ce \
                                where ce.uv_id <> 1 \
                                and ce.fecha between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                and ce.caja_mercaderia is not null \
                                order by ce.fecha asc;"
                
                for c in EntregasPandemia.objects.raw(query_mapa):
                    lista_mapa_caja.append({"uv":c.id-1,"created": str(c.fecha)})
                    
                lista_mapa = lista_mapa_caja

            elif filtro_mapa[categoria] == "Pañal niño":

                lista_mapa_pañal_niño = []
                query_mapa = f"select ce.uv_id as id, ce.fecha \
                                from carga_entregaspandemia ce \
                                where ce.uv_id <> 1 \
                                and ce.fecha between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                and ce.pañal_niño_m is not null \
                                or ce.pañal_niño_g is not null \
                                or ce.pañal_niño_xg is not null \
                                or ce.pañal_niño_xxg is not null \
                                order by ce.fecha asc;"
                
                for c in EntregasPandemia.objects.raw(query_mapa):
                    lista_mapa_pañal_niño.append({"uv":c.id-1,"created": str(c.fecha)})
                    
                lista_mapa = lista_mapa_pañal_niño

            elif filtro_mapa[categoria] == "Pañal adulto":

                lista_mapa_pañal_adulto = []
                query_mapa = f"select ce.uv_id as id, ce.fecha \
                                from carga_entregaspandemia ce \
                                where ce.uv_id <> 1 \
                                and ce.fecha between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                and ce.pañal_adulto is not null \
                                order by ce.fecha asc;"
                
                for c in EntregasPandemia.objects.raw(query_mapa):
                    lista_mapa_pañal_adulto.append({"uv":c.id-1,"created": str(c.fecha)})
                    
                lista_mapa = lista_mapa_pañal_adulto

            elif filtro_mapa[categoria] == "Leche":

                lista_mapa_leche = []
                query_mapa = f"select ce.uv_id as id, ce.fecha \
                                from carga_entregaspandemia ce \
                                where ce.uv_id <> 1 \
                                and ce.fecha between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                and ce.leche_entera is not null \
                                or ce.leche_descremada is not null \
                                order by ce.fecha asc;"
                
                for c in EntregasPandemia.objects.raw(query_mapa):
                    lista_mapa_leche.append({"uv":c.id-1,"created": str(c.fecha)})
                    
                lista_mapa = lista_mapa_leche

            elif filtro_mapa[categoria] == "NAT100":

                lista_mapa_nat = []
                query_mapa = f"select ce.uv_id as id, ce.fecha \
                                from carga_entregaspandemia ce \
                                where ce.uv_id <> 1 \
                                and ce.fecha between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                and ce.nat_100 is not null \
                                order by ce.fecha asc;"
                
                for c in EntregasPandemia.objects.raw(query_mapa):
                    lista_mapa_nat.append({"uv":c.id-1,"created": str(c.fecha)})
                    
                lista_mapa = lista_mapa_nat

            elif filtro_mapa[categoria] == "Balon de Gas":

                lista_mapa_balon = []
                query_mapa = f"select ce.uv_id as id, ce.fecha \
                                from carga_entregaspandemia ce \
                                where ce.uv_id <> 1 \
                                and ce.fecha between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                and ce.balon_gas is not null \
                                order by ce.fecha asc;"
                
                for c in EntregasPandemia.objects.raw(query_mapa):
                    lista_mapa_balon.append({"uv":c.id-1,"created": str(c.fecha)})
                    
                lista_mapa = lista_mapa_balon

            elif filtro_mapa[categoria] == "Parafina":

                lista_mapa_total = []
                query_mapa = f"select ce.uv_id as id, ce.fecha \
                                from carga_entregaspandemia ce \
                                where ce.uv_id <> 1 \
                                and ce.fecha between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                and ce.parafina is not null \
                                order by ce.fecha asc;"
                
                for c in EntregasPandemia.objects.raw(query_mapa):
                    lista_mapa_total.append({"uv":c.id-1,"created": str(c.fecha)})
                    
                lista_mapa = lista_mapa_total
            
            fechas_categoria = {
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'categoria': filtro_mapa[categoria]
            }

            context = {
                'filtro_tiempo':filtro_tiempo,
                'lista_mapa': lista_mapa,
                'diccionario_tabla': diccionario_tabla,
                'fechas_categoria':fechas_categoria
            }

            return render(request,'vis/entrega_pandemia_vis.html', context)

#IMPUESTOS Y DERECHOS (LISTO)
def impuestos_derechos_vis(request,categoria):
    filtro_mapa = [
        "Total",
        "Patente Alcohol",
        "Patente Comercial",
        "Patente Profesional",
        "Patente Industrial",
        "Patente Microempresa",
        "Patente Estacionada"
    ]

    if request.method == 'GET':
        diccionario_tabla = {}
        query_tabla = '''select cu.numero_uv as id,
                            coalesce(alc.cant, 0) + 
                            coalesce(com.cant, 0) + 
                            coalesce(pro.cant, 0) +
                            coalesce(ind.cant, 0) +
                            coalesce(mic.cant, 0) +
                            coalesce(est.cant, 0) as total,
                            case when alc.cant is null then 0 else alc.cant end alc,
                            case when com.cant is null then 0 else com.cant end com,
                            case when pro.cant is null then 0 else pro.cant end pro,
                            case when ind.cant is null then 0 else ind.cant end ind,
                            case when mic.cant is null then 0 else mic.cant end mic,
                            case when est.cant is null then 0 else est.cant end est
                        from core_uv cu
                        left join (
                            select ce.uv_id as uv, count(1) as cant
                            from carga_empresas ce
                            where ce.tipo = 'alcohol'
                            group by ce.uv_id) alc
                            on cu.id = alc.uv
                        left join (
                            select ce.uv_id as uv, count(1) as cant
                            from carga_empresas ce
                            where ce.tipo = 'comercial'
                            group by ce.uv_id) com
                            on cu.id = com.uv
                        left join (
                            select ce.uv_id as uv, count(1) as cant
                            from carga_empresas ce
                            where ce.tipo = 'profesional'
                            group by ce.uv_id) pro
                            on cu.id = pro.uv
                        left join (
                            select ce.uv_id as uv, count(1) as cant
                            from carga_empresas ce
                            where ce.tipo = 'industrial'
                            group by ce.uv_id) ind
                            on cu.id = ind.uv
                        left join (
                            select ce.uv_id as uv, count(1) as cant
                            from carga_empresas ce
                            where ce.tipo = 'microempresa'
                            group by ce.uv_id) mic
                            on cu.id = mic.uv
                        left join (
                            select ce.uv_id as uv, count(1) as cant
                            from carga_empresas ce
                            where ce.tipo = 'estacionado'
                            group by ce.uv_id) est
                            on cu.id = est.uv'''

        for c in Empresas.objects.raw(query_tabla):
            diccionario_tabla[c.id] = [
                c.total,
                c.alc,
                c.com,
                c.pro,
                c.ind,
                c.mic,
                c.est
            ]
        
        #FILTRO POR CATEGORIA 

        if filtro_mapa[categoria] == "Total":

            lista_mapa_total = []
            query_mapa ='''select ce.uv_id as id,
                                ce.created
                            from carga_empresas ce
                            where ce.uv_id <> 0
                            order by ce.created asc;'''
            
            for c in Empresas.objects.raw(query_mapa):
                lista_mapa_total.append({"uv":c.id-1,"created": str(c.created)})
                
            lista_mapa = lista_mapa_total

        elif filtro_mapa[categoria] == "Patente Alcohol":

            lista_mapa_alcohol = []
            query_mapa ='''select ce.uv_id as id,
                                ce.created
                            from carga_empresas ce
                            where ce.uv_id <> 0
                            and ce.tipo = 'alcohol'
                            order by ce.created asc;'''
            
            for c in Empresas.objects.raw(query_mapa):
                lista_mapa_alcohol.append({"uv":c.id-1,"created": str(c.created)})
                
            lista_mapa = lista_mapa_alcohol

        elif filtro_mapa[categoria] == "Patente Comercial":

            lista_mapa_comercial = []
            query_mapa ='''select ce.uv_id as id,
                                ce.created
                            from carga_empresas ce
                            where ce.uv_id <> 0
                            and ce.tipo = 'comercial'
                            order by ce.created asc;'''
            
            for c in Empresas.objects.raw(query_mapa):
                lista_mapa_comercial.append({"uv":c.id-1,"created": str(c.created)})
                
            lista_mapa = lista_mapa_comercial

        elif filtro_mapa[categoria] == "Patente Profesional":

            lista_mapa_profesional = []
            query_mapa ='''select ce.uv_id as id,
                                ce.created
                            from carga_empresas ce
                            where ce.uv_id <> 0
                            and ce.tipo = 'profesional'
                            order by ce.created asc;'''
            
            for c in Empresas.objects.raw(query_mapa):
                lista_mapa_profesional.append({"uv":c.id-1,"created": str(c.created)})
                
            lista_mapa = lista_mapa_profesional

        elif filtro_mapa[categoria] == "Patente Industrial":

            lista_mapa_industial = []
            query_mapa ='''select ce.uv_id as id,
                                ce.created
                            from carga_empresas ce
                            where ce.uv_id <> 0
                            and ce.tipo = 'industrial'
                            order by ce.created asc;'''
            
            for c in Empresas.objects.raw(query_mapa):
                lista_mapa_industial.append({"uv":c.id-1,"created": str(c.created)})
                
            lista_mapa = lista_mapa_industial

        elif filtro_mapa[categoria] == "Patente Microempresa":

            lista_mapa_micro = []
            query_mapa ='''select ce.uv_id as id,
                                ce.created
                            from carga_empresas ce
                            where ce.uv_id <> 0
                            and ce.tipo = 'microempresa'
                            order by ce.created asc;'''
            
            for c in Empresas.objects.raw(query_mapa):
                lista_mapa_micro.append({"uv":c.id-1,"created": str(c.created)})
                
            lista_mapa = lista_mapa_micro

        elif filtro_mapa[categoria] == "Patente Estacionada":

            lista_mapa_estacionada = []
            query_mapa ='''select ce.uv_id as id,
                                ce.created
                            from carga_empresas ce
                            where ce.uv_id <> 0
                            and ce.tipo = 'estacionado'
                            order by ce.created asc;'''
            
            for c in Empresas.objects.raw(query_mapa):
                lista_mapa_estacionada.append({"uv":c.id-1,"created": str(c.created)})
                
            lista_mapa = lista_mapa_estacionada


        tiempo = []
        query_tiempo = '''select 1 as id, max(ce.created) max, min(ce.created) min
                            from(select ce.uv_id as id, ce.created
                            from carga_empresas ce
                            where ce.uv_id <> 0
                            group by ce.uv_id , ce.created 
                            order by ce.created asc) as ce''' #todo se agrego group by 

        for c in Empresas.objects.raw(query_tiempo):
            tiempo = {"max":c.max,"min": c.min}

        fecha_inicio = datetime.strftime(tiempo['min'], '%Y-%m-%d')
        fecha_fin = datetime.strftime(tiempo['max'], '%Y-%m-%d')

        fechas_categoria = {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'categoria': filtro_mapa[categoria]
        }

        filtro_tiempo=FiltroTiempo(fechas_categoria or None)


        context = {
            'filtro_tiempo':filtro_tiempo,
            'lista_mapa': lista_mapa,
            'diccionario_tabla': diccionario_tabla,
            'fechas_categoria': fechas_categoria
        }

        return render(request,'vis/impuestos_derechos_vis.html', context)

    if request.method == 'POST':
        filtro_tiempo=FiltroTiempo(request.POST)

        if filtro_tiempo.is_valid():
            fecha_inicio = filtro_tiempo.cleaned_data.get('fecha_inicio')
            fecha_fin = filtro_tiempo.cleaned_data.get('fecha_fin')

            diccionario_tabla = {}
            query_tabla = f"select cu.numero_uv as id, \
                                coalesce(alc.cant, 0) +  \
                                coalesce(com.cant, 0) +  \
                                coalesce(pro.cant, 0) + \
                                coalesce(ind.cant, 0) + \
                                coalesce(mic.cant, 0) + \
                                coalesce(est.cant, 0) as total, \
                                case when alc.cant is null then 0 else alc.cant end alc, \
                                case when com.cant is null then 0 else com.cant end com, \
                                case when pro.cant is null then 0 else pro.cant end pro, \
                                case when ind.cant is null then 0 else ind.cant end ind, \
                                case when mic.cant is null then 0 else mic.cant end mic, \
                                case when est.cant is null then 0 else est.cant end est \
                            from core_uv cu \
                            left join ( \
                                select ce.uv_id as uv, count(1) as cant \
                                from carga_empresas ce \
                                where ce.tipo = 'alcohol' \
                                and ce.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by ce.uv_id) alc \
                                on cu.id = alc.uv \
                            left join ( \
                                select ce.uv_id as uv, count(1) as cant \
                                from carga_empresas ce \
                                where ce.tipo = 'comercial' \
                                and ce.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by ce.uv_id) com \
                                on cu.id = com.uv \
                            left join ( \
                                select ce.uv_id as uv, count(1) as cant \
                                from carga_empresas ce \
                                where ce.tipo = 'profesional' \
                                and ce.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by ce.uv_id) pro \
                                on cu.id = pro.uv \
                            left join ( \
                                select ce.uv_id as uv, count(1) as cant \
                                from carga_empresas ce \
                                where ce.tipo = 'industrial' \
                                and ce.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by ce.uv_id) ind \
                                on cu.id = ind.uv \
                            left join ( \
                                select ce.uv_id as uv, count(1) as cant \
                                from carga_empresas ce \
                                where ce.tipo = 'microempresa' \
                                and ce.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by ce.uv_id) mic \
                                on cu.id = mic.uv \
                            left join ( \
                                select ce.uv_id as uv, count(1) as cant \
                                from carga_empresas ce \
                                where ce.tipo = 'estacionado' \
                                and ce.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by ce.uv_id) est \
                                on cu.id = est.uv"

            for c in Empresas.objects.raw(query_tabla):
                diccionario_tabla[c.id] = [
                    c.total,
                    c.alc,
                    c.com,
                    c.pro,
                    c.ind,
                    c.mic,
                    c.est
                ]
            
            #FILTRO POR CATEGORIA 

            if filtro_mapa[categoria] == "Total":

                lista_mapa_total = []
                query_mapa =f"select ce.uv_id as id, \
                                    ce.created \
                                from carga_empresas ce \
                                where ce.uv_id <> 0 \
                                and ce.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by ce.created asc;"
                
                for c in Empresas.objects.raw(query_mapa):
                    lista_mapa_total.append({"uv":c.id-1,"created": str(c.created)})
                    
                lista_mapa = lista_mapa_total

            elif filtro_mapa[categoria] == "Patente Alcohol":

                lista_mapa_alcohol = []
                query_mapa =f"select ce.uv_id as id, \
                                    ce.created \
                                from carga_empresas ce \
                                where ce.uv_id <> 0 \
                                and ce.tipo = 'alcohol' \
                                and ce.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by ce.created asc;"
                
                for c in Empresas.objects.raw(query_mapa):
                    lista_mapa_alcohol.append({"uv":c.id-1,"created": str(c.created)})
                    
                lista_mapa = lista_mapa_alcohol

            elif filtro_mapa[categoria] == "Patente Comercial":

                lista_mapa_comercial = []
                query_mapa =f"select ce.uv_id as id, \
                                    ce.created \
                                from carga_empresas ce \
                                where ce.uv_id <> 0 \
                                and ce.tipo = 'comercial' \
                                and ce.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by ce.created asc;"
                
                for c in Empresas.objects.raw(query_mapa):
                    lista_mapa_comercial.append({"uv":c.id-1,"created": str(c.created)})
                    
                lista_mapa = lista_mapa_comercial

            elif filtro_mapa[categoria] == "Patente Profesional":

                lista_mapa_profesional = []
                query_mapa =f"select ce.uv_id as id, \
                                    ce.created \
                                from carga_empresas ce \
                                where ce.uv_id <> 0 \
                                and ce.tipo = 'profesional' \
                                and ce.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by ce.created asc;"
                
                for c in Empresas.objects.raw(query_mapa):
                    lista_mapa_profesional.append({"uv":c.id-1,"created": str(c.created)})
                    
                lista_mapa = lista_mapa_profesional

            elif filtro_mapa[categoria] == "Patente Industrial":

                lista_mapa_industial = []
                query_mapa =f"select ce.uv_id as id, \
                                    ce.created \
                                from carga_empresas ce \
                                where ce.uv_id <> 0 \
                                and ce.tipo = 'industrial' \
                                and ce.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by ce.created asc;"
                
                for c in Empresas.objects.raw(query_mapa):
                    lista_mapa_industial.append({"uv":c.id-1,"created": str(c.created)})
                    
                lista_mapa = lista_mapa_industial

            elif filtro_mapa[categoria] == "Patente Microempresa":

                lista_mapa_micro = []
                query_mapa =f"select ce.uv_id as id, \
                                    ce.created \
                                from carga_empresas ce \
                                where ce.uv_id <> 0 \
                                and ce.tipo = 'microempresa' \
                                and ce.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by ce.created asc;"
                
                for c in Empresas.objects.raw(query_mapa):
                    lista_mapa_micro.append({"uv":c.id-1,"created": str(c.created)})
                    
                lista_mapa = lista_mapa_micro

            elif filtro_mapa[categoria] == "Patente Estacionada":

                lista_mapa_estacionada = []
                query_mapa =f"select ce.uv_id as id, \
                                    ce.created \
                                from carga_empresas ce \
                                where ce.uv_id <> 0 \
                                and ce.tipo = 'estacionado' \
                                and ce.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by ce.created asc;"
                
                for c in Empresas.objects.raw(query_mapa):
                    lista_mapa_estacionada.append({"uv":c.id-1,"created": str(c.created)})
                    
                lista_mapa = lista_mapa_estacionada

            fechas_categoria = {
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'categoria': filtro_mapa[categoria]
            }

            context = {
                'filtro_tiempo':filtro_tiempo,
                'lista_mapa': lista_mapa,
                'diccionario_tabla': diccionario_tabla,
                'fechas_categoria':fechas_categoria
            }

            return render(request,'vis/impuestos_derechos_vis.html', context)

#TRANSITO (LISTO)
def transito_vis(request, categoria):
    filtro_mapa = [
        "Total",
        "Permisos de Circulación",
        "Licencia de Condicir",
    ]

    if request.method == 'GET':

        diccionario_tabla = {}
        query_tabla = '''select cu.numero_uv as id,
                            coalesce(pat.cant, 0) + coalesce(per.cant, 0) as total,
                            coalesce(pat.cant, 0) as pv,
                            coalesce(per.cant, 0) as pc
                        from core_uv cu
                        left join (select lc.uv_id, count(1) as cant
                            from carga_licenciaconducir lc
                            group by lc.uv_id) pat
                            on cu.numero_uv+1 = pat.uv_id
                        left join (select c.uv_id, count(1) as cant
                            from carga_permisoscirculacion c
                            group by c.uv_id) per
                            on cu.numero_uv+1 = per.uv_id;'''

        for c in LicenciaConducir.objects.raw(query_tabla):
            diccionario_tabla[c.id] = [
                c.total,
                c.pc,
                c.pv,
            ]

        #FILTRO POR CATEGORIA 

        if filtro_mapa[categoria] == "Total":
    
            lista_mapa_total = []
            query_mapa = '''SELECT lc.uv_id AS id, lc.fecha AS fecha
                          FROM carga_licenciaconducir lc
                          WHERE lc.uv_id <> 1
                          UNION ALL
                          SELECT c.uv_id AS id, c.fecha AS fecha
                          FROM carga_permisoscirculacion c
                          WHERE c.uv_id <> 1
                          ORDER BY fecha'''


            for c in LicenciaConducir.objects.raw(query_mapa):
                lista_mapa_total.append({"uv":c.id-1,"created": str(c.fecha)})

            lista_mapa = lista_mapa_total

        elif filtro_mapa[categoria] == "Permisos de Circulación":

            lista_mapa_circulacion = []
            query_mapa = '''select c.uv_id as id, c.fecha
                          from carga_permisoscirculacion c
                          where c.uv_id <> 1
                          order by c.fecha asc;'''

            for c in PermisosCirculacion.objects.raw(query_mapa):
                lista_mapa_circulacion.append({"uv":c.id-1,"created": str(c.fecha)})

            lista_mapa = lista_mapa_circulacion

        elif filtro_mapa[categoria] == "Licencia de Condicir":

            lista_mapa_vehicular = []
            query_mapa = '''select lc.uv_id as id, lc.fecha
                          from carga_licenciaconducir lc
                          where lc.uv_id <> 1
                          order by lc.fecha asc;'''

            for c in LicenciaConducir.objects.raw(query_mapa):
                lista_mapa_vehicular.append({"uv":c.id-1,"created": str(c.fecha)})

            lista_mapa = lista_mapa_vehicular

        tiempo = []
        query_tiempo = '''select 1 as id, max(tabla.fecha) max, min(tabla.fecha) min
                          from(SELECT lc.uv_id AS id, lc.fecha AS fecha
                          FROM carga_licenciaconducir lc
                          WHERE lc.uv_id <> 1
                          group by lc.uv_id , lc.fecha 
                          UNION ALL
                          SELECT c.uv_id AS id, c.fecha AS fecha
                          FROM carga_permisoscirculacion c
                          WHERE c.uv_id <> 1
                          group by c.uv_id, c.fecha 
                          ORDER BY fecha) tabla''' #todo se agrego group by


        for c in LicenciaConducir.objects.raw(query_tiempo):
            tiempo = {"max":c.max,"min": c.min}

        fecha_inicio = datetime.strftime(tiempo['min'], '%Y-%m-%d')
        fecha_fin = datetime.strftime(tiempo['max'], '%Y-%m-%d')

        fechas_categoria = {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'categoria': filtro_mapa[categoria]
        }

        filtro_tiempo=FiltroTiempo(fechas_categoria or None)

        context = {
            'filtro_tiempo':filtro_tiempo,
            'lista_mapa': lista_mapa,
            'diccionario_tabla': diccionario_tabla,
            'fechas_categoria': fechas_categoria
        }

        return render(request,'vis/transito_vis.html',context)

    if request.method == 'POST':
        filtro_tiempo=FiltroTiempo(request.POST)

        if filtro_tiempo.is_valid():
            fecha_inicio = filtro_tiempo.cleaned_data.get('fecha_inicio')
            fecha_fin = filtro_tiempo.cleaned_data.get('fecha_fin')

            diccionario_tabla = {}
            query_tabla = f"select cu.numero_uv as id, \
                            coalesce(pat.cant, 0) + coalesce(per.cant, 0) as total, \
                            coalesce(pat.cant, 0) as lc, \
                            coalesce(per.cant, 0) as pc \
                        from core_uv cu \
                        left join (select lc.uv_id, count(1) as cant \
                            from carga_licenciaconducir lc \
                            where lc.fecha between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            group by lc.uv_id) pat \
                            on cu.numero_uv+1 = pat.uv_id \
                        left join (select c.uv_id, count(1) as cant \
                            from carga_permisoscirculacion c \
                            where c.fecha between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            group by c.uv_id) per \
                            on cu.numero_uv+1 = per.uv_id;"

            for c in LicenciaConducir.objects.raw(query_tabla):
                diccionario_tabla[c.id] = [
                    c.total,
                    c.pc,
                    c.lc,
                ]

            #FILTRO POR CATEGORIA 

            if filtro_mapa[categoria] == "Total":

                lista_mapa_total = []
                query_mapa = f"SELECT lc.uv_id AS id, lc.fecha AS fecha \
                            FROM carga_licenciaconducir lc \
                            WHERE lc.uv_id <> 1 \
                            AND lc.fecha BETWEEN \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            UNION ALL \
                            SELECT c.uv_id AS id, c.fecha AS fecha \
                            FROM carga_permisoscirculacion c \
                            WHERE c.uv_id <> 1 \
                            AND c.fecha BETWEEN \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            ORDER BY fecha"

                for c in LicenciaConducir.objects.raw(query_mapa):
                    lista_mapa_total.append({"uv":c.id-1,"created": str(c.fecha)})

                lista_mapa = lista_mapa_total

            elif filtro_mapa[categoria] == "Permisos de Circulación":

                lista_mapa_circulacion = []
                query_mapa = f"select c.uv_id as id, c.fecha \
                            from carga_permisoscirculacion c \
                            where c.uv_id <> 1 \
                            and c.fecha between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            order by c.fecha asc;"

                for c in PermisosCirculacion.objects.raw(query_mapa):
                    lista_mapa_circulacion.append({"uv":c.id-1,"created": str(c.fecha)})

                lista_mapa = lista_mapa_circulacion

            elif filtro_mapa[categoria] == "Licencia de Condicir":

                lista_mapa_vehicular = []
                query_mapa = f"select lc.uv_id as id, lc.fecha \
                            from carga_licenciaconducir lc \
                            where lc.uv_id <> 1 \
                            and lc.fecha between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                            order by lc.fecha asc;"

                for c in LicenciaConducir.objects.raw(query_mapa):
                    lista_mapa_vehicular.append({"uv":c.id-1,"created": str(c.fecha)})

                lista_mapa = lista_mapa_vehicular

            fechas_categoria = {
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'categoria': filtro_mapa[categoria]
            }

            context = {
                'filtro_tiempo':filtro_tiempo,
                'lista_mapa': lista_mapa,
                'diccionario_tabla': diccionario_tabla,
                'fechas_categoria':fechas_categoria
            }

            return render(request,'vis/transito_vis.html',context)

#OBRAS MUNICIPALES (DOM)
def obras_municipales_vis(request,categoria):
    filtro_mapa = [
        "Total",
        "ANEXIÓN",
        "ANTIGUAS",
        "ANULACION",
        "CAMBIO DE DESTINO",
        "FUSIÓN",
        "LEY 20,898",
        "OBRAS MENORES",
        "PERMISO DE EDIFICACIÓN",
        "RECEPCIÓN FINAL",
        "REGULARIZACIONES",
        "REGULARIZACIONES LEY 18.591",
        "RESOLUCIÓN",
        "SUBDIVISIONES",
        "VENTA POR PISO",
    ]

    if request.method == 'GET':
        diccionario_tabla = {}
        query_tabla ='''select cu.numero_uv as id,
                            coalesce(anx.cant, 0) + 
                            coalesce(ant.cant, 0) + 
                            coalesce(anu.cant, 0) +
                            coalesce(cdd.cant, 0) +
                            coalesce(cdd.cant, 0) +
                            coalesce(fsn.cant, 0) +
                            coalesce(ley.cant, 0) +
                            coalesce(oms.cant, 0) +
                            coalesce(pde.cant, 0) +
                            coalesce(rfl.cant, 0) +
                            coalesce(rgl.cant, 0) +
                            coalesce(rley.cant, 0) +
                            coalesce(rsl.cant, 0) +
                            coalesce(sdv.cant, 0) +
                            coalesce(vpp.cant, 0) as total,
                            case when anx.cant is null then 0 else anx.cant end anx,
                            case when ant.cant is null then 0 else ant.cant end ant,
                            case when anu.cant is null then 0 else anu.cant end anu,
                            case when cdd.cant is null then 0 else cdd.cant end cdd,
                            case when fsn.cant is null then 0 else fsn.cant end fsn,
                            case when ley.cant is null then 0 else ley.cant end ley,
                            case when oms.cant is null then 0 else oms.cant end oms,
                            case when pde.cant is null then 0 else pde.cant end pde,
                            case when rfl.cant is null then 0 else rfl.cant end rfl,
                            case when rgl.cant is null then 0 else rgl.cant end rgl,
                            case when rley.cant is null then 0 else rley.cant end rley,
                            case when rsl.cant is null then 0 else rsl.cant end rsl,
                            case when sdv.cant is null then 0 else sdv.cant end sdv,
                            case when vpp.cant is null then 0 else vpp.cant end vpp
                        from core_uv cu
                        left join (select cd.uv_id as uv, count(1) as cant
                            from carga_dom cd 
                            where cd.tramite = 'ANEXIÓN'
                            group by cd.uv_id) anx
                            on cu.id = anx.uv
                        left join (select cd.uv_id as uv, count(1) as cant
                            from carga_dom cd 
                            where cd.tramite = 'ANTIGUAS'
                            group by cd.uv_id) ant
                            on cu.id = ant.uv
                        left join (select cd.uv_id as uv, count(1) as cant
                            from carga_dom cd 
                            where cd.tramite = 'ANULACION'
                            group by cd.uv_id) anu
                            on cu.id = anu.uv
                        left join (select cd.uv_id as uv, count(1) as cant
                            from carga_dom cd 
                            where cd.tramite = 'CAMBIO DE DESTINO'
                            group by cd.uv_id) cdd
                            on cu.id = cdd.uv
                        left join (select cd.uv_id as uv, count(1) as cant
                            from carga_dom cd 
                            where cd.tramite = 'FUSIÓN'
                            group by cd.uv_id) fsn
                            on cu.id = fsn.uv
                        left join (select cd.uv_id as uv, count(1) as cant
                            from carga_dom cd 
                            where cd.tramite = 'LEY 20,898'
                            group by cd.uv_id) ley
                            on cu.id = ley.uv
                        left join (select cd.uv_id as uv, count(1) as cant
                            from carga_dom cd 
                            where cd.tramite = 'OBRAS MENORES'
                            group by cd.uv_id) oms
                            on cu.id = oms.uv
                        left join (select cd.uv_id as uv, count(1) as cant
                            from carga_dom cd 
                            where cd.tramite = 'PERMISO DE EDIFICACIÓN'
                            group by cd.uv_id) pde
                            on cu.id = pde.uv
                        left join (select cd.uv_id as uv, count(1) as cant
                            from carga_dom cd 
                            where cd.tramite = 'RECEPCIÓN FINAL'
                            group by cd.uv_id) rfl
                            on cu.id = rfl.uv
                        left join (select cd.uv_id as uv, count(1) as cant
                            from carga_dom cd 
                            where cd.tramite = 'REGULARIZACIONES'
                            group by cd.uv_id) rgl
                            on cu.id = rgl.uv
                        left join (select cd.uv_id as uv, count(1) as cant
                            from carga_dom cd 
                            where cd.tramite = 'REGULARIZACIONES LEY 18.591'
                            group by cd.uv_id) rley
                            on cu.id = rley.uv
                        left join (select cd.uv_id as uv, count(1) as cant
                            from carga_dom cd 
                            where cd.tramite = 'RESOLUCIÓN'
                            group by cd.uv_id) rsl
                            on cu.id = rsl.uv
                        left join (select cd.uv_id as uv, count(1) as cant
                            from carga_dom cd 
                            where cd.tramite = 'SUBDIVISIONES'
                            group by cd.uv_id) sdv
                            on cu.id = sdv.uv
                        left join (select cd.uv_id as uv, count(1) as cant
                            from carga_dom cd 
                            where cd.tramite = 'VENTA POR PISO'
                            group by cd.uv_id) vpp
                            on cu.id = vpp.uv'''

        for c in DOM.objects.raw(query_tabla):
            diccionario_tabla[c.id] = [
                c.total,
                c.anx,
                c.ant,
                c.anu,
                c.cdd,
                c.fsn,
                c.ley,
                c.oms,
                c.pde,
                c.rfl,
                c.rgl,
                c.rley,
                c.rsl,
                c.sdv,
                c.vpp,
            ]

        #FILTRO POR CATEGORIA 

        if filtro_mapa[categoria] == "Total":
            lista_mapa_total = []
            query_mapa  ='''select cd.uv_id as id,
                                cd.created 
                            from carga_dom cd
                            where cd.uv_id <> 0
                            order by cd.created asc;'''

            for c in DOM.objects.raw(query_mapa):
                lista_mapa_total.append({"uv":c.id-1,"created": str(c.created)})

            lista_mapa = lista_mapa_total

        elif filtro_mapa[categoria] == "ANEXIÓN":
            lista_mapa_anexion = []
            query_mapa  ='''select cd.uv_id as id,
                                cd.created 
                            from carga_dom cd
                            where cd.uv_id <> 0
                            and cd.tramite = 'ANEXIÓN'
                            order by cd.created asc;'''

            for c in DOM.objects.raw(query_mapa):
                lista_mapa_anexion.append({"uv":c.id-1,"created": str(c.created)})

            lista_mapa = lista_mapa_anexion

        elif filtro_mapa[categoria] == "ANTIGUAS":
            lista_mapa_antiguas = []
            query_mapa  ='''select cd.uv_id as id,
                                cd.created 
                            from carga_dom cd
                            where cd.uv_id <> 0
                            and cd.tramite = 'ANTIGUAS'
                            order by cd.created asc;'''

            for c in DOM.objects.raw(query_mapa):
                lista_mapa_antiguas.append({"uv":c.id-1,"created": str(c.created)})

            lista_mapa = lista_mapa_antiguas

        elif filtro_mapa[categoria] == "ANULACION":
            lista_mapa_anulacion = []
            query_mapa  ='''select cd.uv_id as id,
                                cd.created 
                            from carga_dom cd
                            where cd.uv_id <> 0
                            and cd.tramite = 'ANULACION'
                            order by cd.created asc;'''

            for c in DOM.objects.raw(query_mapa):
                lista_mapa_anulacion.append({"uv":c.id-1,"created": str(c.created)})

            lista_mapa = lista_mapa_anulacion

        elif filtro_mapa[categoria] == "CAMBIO DE DESTINO":
            lista_mapa_cambio = []
            query_mapa  ='''select cd.uv_id as id,
                                cd.created 
                            from carga_dom cd
                            where cd.uv_id <> 0
                            and cd.tramite = 'CAMBIO DE DESTINO'
                            order by cd.created asc;'''

            for c in DOM.objects.raw(query_mapa):
                lista_mapa_cambio.append({"uv":c.id-1,"created": str(c.created)})

            lista_mapa = lista_mapa_cambio

        elif filtro_mapa[categoria] == "FUSIÓN":
            lista_mapa_fusion = []
            query_mapa  ='''select cd.uv_id as id,
                                cd.created 
                            from carga_dom cd
                            where cd.uv_id <> 0
                            and cd.tramite = 'FUSIÓN'
                            order by cd.created asc;'''

            for c in DOM.objects.raw(query_mapa):
                lista_mapa_fusion.append({"uv":c.id-1,"created": str(c.created)})

            lista_mapa = lista_mapa_fusion

        elif filtro_mapa[categoria] == "LEY 20,898":
            lista_mapa_ley = []
            query_mapa  ='''select cd.uv_id as id,
                                cd.created 
                            from carga_dom cd
                            where cd.uv_id <> 0
                            and cd.tramite = 'LEY 20,898'
                            order by cd.created asc;'''

            for c in DOM.objects.raw(query_mapa):
                lista_mapa_ley.append({"uv":c.id-1,"created": str(c.created)})

            lista_mapa = lista_mapa_ley

        elif filtro_mapa[categoria] == "OBRAS MENORES":
            lista_mapa_obras = []
            query_mapa  ='''select cd.uv_id as id,
                                cd.created 
                            from carga_dom cd
                            where cd.uv_id <> 0
                            and cd.tramite = 'OBRAS MENORES'
                            order by cd.created asc;'''

            for c in DOM.objects.raw(query_mapa):
                lista_mapa_obras.append({"uv":c.id-1,"created": str(c.created)})

            lista_mapa = lista_mapa_obras

        elif filtro_mapa[categoria] == "PERMISO DE EDIFICACIÓN":
            lista_mapa_edificacion = []
            query_mapa  ='''select cd.uv_id as id,
                                cd.created 
                            from carga_dom cd
                            where cd.uv_id <> 0
                            and cd.tramite = 'PERMISO DE EDIFICACIÓN'
                            order by cd.created asc;'''

            for c in DOM.objects.raw(query_mapa):
                lista_mapa_edificacion.append({"uv":c.id-1,"created": str(c.created)})

            lista_mapa = lista_mapa_edificacion

        elif filtro_mapa[categoria] == "RECEPCIÓN FINAL":
            lista_mapa_recepcion = []
            query_mapa  ='''select cd.uv_id as id,
                                cd.created 
                            from carga_dom cd
                            where cd.uv_id <> 0
                            and cd.tramite = 'RECEPCIÓN FINAL'
                            order by cd.created asc;'''

            for c in DOM.objects.raw(query_mapa):
                lista_mapa_recepcion.append({"uv":c.id-1,"created": str(c.created)})

            lista_mapa = lista_mapa_recepcion

        elif filtro_mapa[categoria] == "REGULARIZACIONES":
            lista_mapa_regularizaciones = []
            query_mapa  ='''select cd.uv_id as id,
                                cd.created 
                            from carga_dom cd
                            where cd.uv_id <> 0
                            and cd.tramite = 'REGULARIZACIONES'
                            order by cd.created asc;'''

            for c in DOM.objects.raw(query_mapa):
                lista_mapa_regularizaciones.append({"uv":c.id-1,"created": str(c.created)})

            lista_mapa = lista_mapa_regularizaciones

        elif filtro_mapa[categoria] == "REGULARIZACIONES LEY 18.591":
            lista_mapa_reg_ley = []
            query_mapa  ='''select cd.uv_id as id,
                                cd.created 
                            from carga_dom cd
                            where cd.uv_id <> 0
                            and cd.tramite = 'REGULARIZACIONES LEY 18.591'
                            order by cd.created asc;'''

            for c in DOM.objects.raw(query_mapa):
                lista_mapa_reg_ley.append({"uv":c.id-1,"created": str(c.created)})

            lista_mapa = lista_mapa_reg_ley

        elif filtro_mapa[categoria] == "RESOLUCIÓN":
            lista_mapa_resolucion = []
            query_mapa  ='''select cd.uv_id as id,
                                cd.created 
                            from carga_dom cd
                            where cd.uv_id <> 0
                            and cd.tramite = 'RESOLUCIÓN'
                            order by cd.created asc;'''

            for c in DOM.objects.raw(query_mapa):
                lista_mapa_resolucion.append({"uv":c.id-1,"created": str(c.created)})

            lista_mapa = lista_mapa_resolucion

        elif filtro_mapa[categoria] == "SUBDIVISIONES":
            lista_mapa_subdivisiones = []
            query_mapa  ='''select cd.uv_id as id,
                                cd.created 
                            from carga_dom cd
                            where cd.uv_id <> 0
                            and cd.tramite = 'SUBDIVISIONES'
                            order by cd.created asc;'''

            for c in DOM.objects.raw(query_mapa):
                lista_mapa_subdivisiones.append({"uv":c.id-1,"created": str(c.created)})

            lista_mapa = lista_mapa_subdivisiones

        elif filtro_mapa[categoria] == "VENTA POR PISO":
            lista_mapa_venta = []
            query_mapa  ='''select cd.uv_id as id,
                                cd.created 
                            from carga_dom cd
                            where cd.uv_id <> 0
                            and cd.tramite = 'VENTA POR PISO'
                            order by cd.created asc;'''

            for c in DOM.objects.raw(query_mapa):
                lista_mapa_venta.append({"uv":c.id-1,"created": str(c.created)})

            lista_mapa = lista_mapa_venta


        tiempo = []
        query_tiempo = '''select 1 as id, min(cd.created) min, max(cd.created) max
	                        from(select cd.uv_id as id, cd.created
                            from carga_dom cd
                            where cd.uv_id <> 0
                            group by cd.uv_id, cd.created 
                            order by cd.created asc) as cd;'''


        for c in DOM.objects.raw(query_tiempo):
            tiempo = {"max":c.max,"min": c.min}

        fecha_inicio = datetime.strftime(tiempo['min'], '%Y-%m-%d')
        fecha_fin = datetime.strftime(tiempo['max'], '%Y-%m-%d')

        fechas_categoria = {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'categoria': filtro_mapa[categoria]
        }

        filtro_tiempo=FiltroTiempo(fechas_categoria or None)

        context = {
            'filtro_tiempo':filtro_tiempo,
            'lista_mapa': lista_mapa,
            'diccionario_tabla': diccionario_tabla,
            'fechas_categoria': fechas_categoria
        }

        return render (request,'vis/dom_vis.html', context)

    if request.method == 'POST':
        filtro_tiempo=FiltroTiempo(request.POST)

        if filtro_tiempo.is_valid():
            fecha_inicio = filtro_tiempo.cleaned_data.get('fecha_inicio')
            fecha_fin = filtro_tiempo.cleaned_data.get('fecha_fin')

            diccionario_tabla = {}
            query_tabla =f"select cu.numero_uv as id, \
                                coalesce(anx.cant, 0) + \
                                coalesce(ant.cant, 0) + \
                                coalesce(anu.cant, 0) + \
                                coalesce(cdd.cant, 0) + \
                                coalesce(cdd.cant, 0) + \
                                coalesce(fsn.cant, 0) + \
                                coalesce(ley.cant, 0) + \
                                coalesce(oms.cant, 0) + \
                                coalesce(pde.cant, 0) + \
                                coalesce(rfl.cant, 0) + \
                                coalesce(rgl.cant, 0) + \
                                coalesce(rley.cant, 0) + \
                                coalesce(rsl.cant, 0) + \
                                coalesce(sdv.cant, 0) + \
                                coalesce(vpp.cant, 0) as total, \
                                case when anx.cant is null then 0 else anx.cant end anx, \
                                case when ant.cant is null then 0 else ant.cant end ant, \
                                case when anu.cant is null then 0 else anu.cant end anu, \
                                case when cdd.cant is null then 0 else cdd.cant end cdd, \
                                case when fsn.cant is null then 0 else fsn.cant end fsn, \
                                case when ley.cant is null then 0 else ley.cant end ley, \
                                case when oms.cant is null then 0 else oms.cant end oms, \
                                case when pde.cant is null then 0 else pde.cant end pde, \
                                case when rfl.cant is null then 0 else rfl.cant end rfl, \
                                case when rgl.cant is null then 0 else rgl.cant end rgl, \
                                case when rley.cant is null then 0 else rley.cant end rley,  \
                                case when rsl.cant is null then 0 else rsl.cant end rsl, \
                                case when sdv.cant is null then 0 else sdv.cant end sdv, \
                                case when vpp.cant is null then 0 else vpp.cant end vpp \
                            from core_uv cu \
                            left join (select cd.uv_id as uv, count(1) as cant \
                                from carga_dom cd  \
                                where cd.tramite = 'ANEXIÓN' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by cd.uv_id) anx \
                                on cu.id = anx.uv \
                            left join (select cd.uv_id as uv, count(1) as cant \
                                from carga_dom cd  \
                                where cd.tramite = 'ANTIGUAS' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by cd.uv_id) ant \
                                on cu.id = ant.uv \
                            left join (select cd.uv_id as uv, count(1) as cant \
                                from carga_dom cd  \
                                where cd.tramite = 'ANULACION' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by cd.uv_id) anu  \
                                on cu.id = anu.uv \
                            left join (select cd.uv_id as uv, count(1) as cant \
                                from carga_dom cd  \
                                where cd.tramite = 'CAMBIO DE DESTINO' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by cd.uv_id) cdd \
                                on cu.id = cdd.uv \
                            left join (select cd.uv_id as uv, count(1) as cant \
                                from carga_dom cd  \
                                where cd.tramite = 'FUSIÓN' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by cd.uv_id) fsn \
                                on cu.id = fsn.uv \
                            left join (select cd.uv_id as uv, count(1) as cant \
                                from carga_dom cd  \
                                where cd.tramite = 'LEY 20,898' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by cd.uv_id) ley \
                                on cu.id = ley.uv \
                            left join (select cd.uv_id as uv, count(1) as cant \
                                from carga_dom cd  \
                                where cd.tramite = 'OBRAS MENORES' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by cd.uv_id) oms \
                                on cu.id = oms.uv \
                            left join (select cd.uv_id as uv, count(1) as cant \
                                from carga_dom cd  \
                                where cd.tramite = 'PERMISO DE EDIFICACIÓN' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by cd.uv_id) pde \
                                on cu.id = pde.uv \
                            left join (select cd.uv_id as uv, count(1) as cant \
                                from carga_dom cd  \
                                where cd.tramite = 'RECEPCIÓN FINAL' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by cd.uv_id) rfl \
                                on cu.id = rfl.uv \
                            left join (select cd.uv_id as uv, count(1) as cant \
                                from carga_dom cd  \
                                where cd.tramite = 'REGULARIZACIONES' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by cd.uv_id) rgl \
                                on cu.id = rgl.uv \
                            left join (select cd.uv_id as uv, count(1) as cant \
                                from carga_dom cd  \
                                where cd.tramite = 'REGULARIZACIONES LEY 18.591' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by cd.uv_id) rley \
                                on cu.id = rley.uv \
                            left join (select cd.uv_id as uv, count(1) as cant \
                                from carga_dom cd  \
                                where cd.tramite = 'RESOLUCIÓN' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by cd.uv_id) rsl \
                                on cu.id = rsl.uv \
                            left join (select cd.uv_id as uv, count(1) as cant \
                                from carga_dom cd \
                                where cd.tramite = 'SUBDIVISIONES' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by cd.uv_id) sdv \
                                on cu.id = sdv.uv \
                            left join (select cd.uv_id as uv, count(1) as cant \
                                from carga_dom cd  \
                                where cd.tramite = 'VENTA POR PISO' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                group by cd.uv_id) vpp \
                                on cu.id = vpp.uv"

            for c in DOM.objects.raw(query_tabla):
                diccionario_tabla[c.id] = [
                    c.total,
                    c.anx,
                    c.ant,
                    c.anu,
                    c.cdd,
                    c.fsn,
                    c.ley,
                    c.oms,
                    c.pde,
                    c.rfl,
                    c.rgl,
                    c.rley,
                    c.rsl,
                    c.sdv,
                    c.vpp,
                ]

            #FILTRO POR CATEGORIA 

            if filtro_mapa[categoria] == "Total":
                lista_mapa_total = []
                query_mapa  =f"select cd.uv_id as id, \
                                    cd.created  \
                                from carga_dom cd \
                                where cd.uv_id <> 0 \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by cd.created asc;"

                for c in DOM.objects.raw(query_mapa):
                    lista_mapa_total.append({"uv":c.id-1,"created": str(c.created)})

                lista_mapa = lista_mapa_total

            elif filtro_mapa[categoria] == "ANEXIÓN":
                lista_mapa_anexion = []
                query_mapa  =f"select cd.uv_id as id, \
                                    cd.created  \
                                from carga_dom cd \
                                where cd.uv_id <> 0 \
                                and cd.tramite = 'ANEXIÓN' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by cd.created asc;"

                for c in DOM.objects.raw(query_mapa):
                    lista_mapa_anexion.append({"uv":c.id-1,"created": str(c.created)})

                lista_mapa = lista_mapa_anexion

            elif filtro_mapa[categoria] == "ANTIGUAS":
                lista_mapa_antiguas = []
                query_mapa  =f"select cd.uv_id as id, \
                                    cd.created  \
                                from carga_dom cd \
                                where cd.uv_id <> 0 \
                                and cd.tramite = 'ANTIGUAS' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by cd.created asc;"

                for c in DOM.objects.raw(query_mapa):
                    lista_mapa_antiguas.append({"uv":c.id-1,"created": str(c.created)})

                lista_mapa = lista_mapa_antiguas

            elif filtro_mapa[categoria] == "ANULACION":
                lista_mapa_anulacion = []
                query_mapa  =f"select cd.uv_id as id, \
                                    cd.created  \
                                from carga_dom cd \
                                where cd.uv_id <> 0 \
                                and cd.tramite = 'ANULACION' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by cd.created asc;"

                for c in DOM.objects.raw(query_mapa):
                    lista_mapa_anulacion.append({"uv":c.id-1,"created": str(c.created)})

                lista_mapa = lista_mapa_anulacion

            elif filtro_mapa[categoria] == "CAMBIO DE DESTINO":
                lista_mapa_cambio = []
                query_mapa  =f"select cd.uv_id as id, \
                                    cd.created  \
                                from carga_dom cd \
                                where cd.uv_id <> 0 \
                                and cd.tramite = 'CAMBIO DE DESTINO' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by cd.created asc;"

                for c in DOM.objects.raw(query_mapa):
                    lista_mapa_cambio.append({"uv":c.id-1,"created": str(c.created)})

                lista_mapa = lista_mapa_cambio

            elif filtro_mapa[categoria] == "FUSIÓN":
                lista_mapa_fusion = []
                query_mapa  =f"select cd.uv_id as id, \
                                    cd.created  \
                                from carga_dom cd \
                                where cd.uv_id <> 0 \
                                and cd.tramite = 'FUSIÓN' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by cd.created asc;"

                for c in DOM.objects.raw(query_mapa):
                    lista_mapa_fusion.append({"uv":c.id-1,"created": str(c.created)})

                lista_mapa = lista_mapa_fusion

            elif filtro_mapa[categoria] == "LEY 20,898":
                lista_mapa_ley = []
                query_mapa  =f"select cd.uv_id as id, \
                                    cd.created  \
                                from carga_dom cd \
                                where cd.uv_id <> 0 \
                                and cd.tramite = 'LEY 20,898' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by cd.created asc;"

                for c in DOM.objects.raw(query_mapa):
                    lista_mapa_ley.append({"uv":c.id-1,"created": str(c.created)})

                lista_mapa = lista_mapa_ley

            elif filtro_mapa[categoria] == "OBRAS MENORES":
                lista_mapa_obras = []
                query_mapa  =f"select cd.uv_id as id, \
                                    cd.created  \
                                from carga_dom cd \
                                where cd.uv_id <> 0 \
                                and cd.tramite = 'OBRAS MENORES' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by cd.created asc;"

                for c in DOM.objects.raw(query_mapa):
                    lista_mapa_obras.append({"uv":c.id-1,"created": str(c.created)})

                lista_mapa = lista_mapa_obras

            elif filtro_mapa[categoria] == "PERMISO DE EDIFICACIÓN":
                lista_mapa_edificacion = []
                query_mapa  =f"select cd.uv_id as id, \
                                    cd.created  \
                                from carga_dom cd \
                                where cd.uv_id <> 0 \
                                and cd.tramite = 'PERMISO DE EDIFICACIÓN' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by cd.created asc;"

                for c in DOM.objects.raw(query_mapa):
                    lista_mapa_edificacion.append({"uv":c.id-1,"created": str(c.created)})

                lista_mapa = lista_mapa_edificacion

            elif filtro_mapa[categoria] == "RECEPCIÓN FINAL":
                lista_mapa_recepcion = []
                query_mapa  =f"select cd.uv_id as id, \
                                    cd.created  \
                                from carga_dom cd \
                                where cd.uv_id <> 0 \
                                and cd.tramite = 'RECEPCIÓN FINAL' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by cd.created asc;"

                for c in DOM.objects.raw(query_mapa):
                    lista_mapa_recepcion.append({"uv":c.id-1,"created": str(c.created)})

                lista_mapa = lista_mapa_recepcion

            elif filtro_mapa[categoria] == "REGULARIZACIONES":
                lista_mapa_regularizaciones = []
                query_mapa  =f"select cd.uv_id as id, \
                                    cd.created  \
                                from carga_dom cd \
                                where cd.uv_id <> 0 \
                                and cd.tramite = 'REGULARIZACIONES' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by cd.created asc;"

                for c in DOM.objects.raw(query_mapa):
                    lista_mapa_regularizaciones.append({"uv":c.id-1,"created": str(c.created)})

                lista_mapa = lista_mapa_regularizaciones

            elif filtro_mapa[categoria] == "REGULARIZACIONES LEY 18.591":
                lista_mapa_reg_ley = []
                query_mapa  =f"select cd.uv_id as id, \
                                    cd.created  \
                                from carga_dom cd \
                                where cd.uv_id <> 0 \
                                and cd.tramite = 'REGULARIZACIONES LEY 18.591' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by cd.created asc;"

                for c in DOM.objects.raw(query_mapa):
                    lista_mapa_reg_ley.append({"uv":c.id-1,"created": str(c.created)})

                lista_mapa = lista_mapa_reg_ley

            elif filtro_mapa[categoria] == "RESOLUCIÓN":
                lista_mapa_resolucion = []
                query_mapa  =f"select cd.uv_id as id, \
                                    cd.created  \
                                from carga_dom cd \
                                where cd.uv_id <> 0 \
                                and cd.tramite = 'RESOLUCIÓN' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by cd.created asc;"

                for c in DOM.objects.raw(query_mapa):
                    lista_mapa_resolucion.append({"uv":c.id-1,"created": str(c.created)})

                lista_mapa = lista_mapa_resolucion

            elif filtro_mapa[categoria] == "SUBDIVISIONES":
                lista_mapa_subdivisiones = []
                query_mapa  =f"select cd.uv_id as id, \
                                    cd.created  \
                                from carga_dom cd \
                                where cd.uv_id <> 0 \
                                and cd.tramite = 'SUBDIVISIONES' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by cd.created asc;"

                for c in DOM.objects.raw(query_mapa):
                    lista_mapa_subdivisiones.append({"uv":c.id-1,"created": str(c.created)})

                lista_mapa = lista_mapa_subdivisiones

            elif filtro_mapa[categoria] == "VENTA POR PISO":
                lista_mapa_venta = []
                query_mapa  =f"select cd.uv_id as id, \
                                    cd.created  \
                                from carga_dom cd \
                                where cd.uv_id <> 0 \
                                and cd.tramite = 'VENTA POR PISO' \
                                and cd.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                order by cd.created asc;"

                for c in DOM.objects.raw(query_mapa):
                    lista_mapa_venta.append({"uv":c.id-1,"created": str(c.created)})

                lista_mapa = lista_mapa_venta

            fechas_categoria = {
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'categoria': filtro_mapa[categoria]
            }

            context = {
                'filtro_tiempo':filtro_tiempo,
                'lista_mapa': lista_mapa,
                'diccionario_tabla': diccionario_tabla,
                'fechas_categoria':fechas_categoria
            }

            return render (request,'vis/dom_vis.html', context)
