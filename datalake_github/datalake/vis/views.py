import pandas as pd
import os
import boto3
import json

from django.shortcuts import render, redirect

from .forms import(
    FiltroTiempo,
)
from core.models import(
    UV,
    Direccion,
    Persona,
)
from farmacia.models import(
    ComprobanteVenta,
)
from dimap.models import(
    ControlPlaga,
    Procedimiento,
    SeguridadDIMAP,
)
from seguridad.models import(
    Requerimiento,
)
from carga.models import(
    EntregasPandemia,
)


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
    
    # archivo = VisFarmacia.objects.get(pk=1)

    # s3_client = boto3.client(
    #     's3',
    #     aws_access_key_id = AWS_ACCESS_KEY_ID,
    #     aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    # )
    # obj = s3_client.get_object(
    #     Bucket = AWS_STORAGE_BUCKET_NAME,
    #     # Key = 'media/vis/data/farmacia/TABLA_FARMACIA.csv',
    #     Key = 'media/vis/data/farmacia/MAPA_FARMACIA.csv',
    # )
    # df_farmacia = pd.read_csv(obj['Body'])

    # diccionario={}
    # uv_cantidad = 28
    # for uv in range(uv_cantidad):
    #     # diccionario[f'{uv}'] = 0        #DEPENDIENDO DE QUE TIPO DE VALOR SEA UV EN DJANGO
    #     diccionario[uv] = 0
    # uv_df = df_farmacia['uv']
    # df = df_farmacia['cant']
    # for key in uv_df.index:
    #     diccionario[key] = df[key]
    # df_mapa = pd.read_csv(obj['Body'], encoding='utf-8')
    # mapa_json = json.loads(df_mapa.to_json(orient="split"))
    # comprobante_venta = ComprobanteVenta.objects.all()
    # persona = Persona.objects.all()
    # print(ComprobanteVenta.objects.select_related('comprador').all().values())

    filtro_tiempo=FiltroTiempo()
    if request.method == 'POST':
        filtro_tiempo=FiltroTiempo(request.POST)
        if filtro_tiempo.is_valid():
            fecha_inicio = filtro_tiempo.cleaned_data.get('fecha_inicio')
            fecha_fin = filtro_tiempo.cleaned_data.get('fecha_fin')
            mapa_json = []
            for r in ComprobanteVenta.objects.raw(f"select fc.id, p.nombre_persona ,u.numero_uv, fc.created \
                                                    from farmacia_comprobanteventa fc \
                                                    left join core_persona p \
                                                        on fc.comprador_id = p.id \
                                                    left join core_uv u \
                                                        on p.uv_id = u.id \
                                                    where fc.created between \'{fecha_inicio}\' and \'{fecha_fin}\' \
                                                    order by fc.created asc;"):
                mapa_json.append({"uv":r.numero_uv,"created": str(r.created)})
            prueba_diccionario = mapa_json

            context = {
                # 'archivo':archivo,
                # 'diccionario':diccionario,
                'filtro_tiempo':filtro_tiempo,
                'prueba_diccionario':prueba_diccionario,
                # 'contador':contador_dir
                

            }
            
            return render(request,'vis/farmacia_vis.html', context)


    
    else:

        mapa_json = []
        for r in ComprobanteVenta.objects.raw('''select fc.id, p.nombre_persona ,u.numero_uv, fc.created
                                                from farmacia_comprobanteventa fc
                                                left join core_persona p
                                                    on fc.comprador_id = p.id
                                                left join core_uv u
                                                    on p.uv_id = u.id 
                                                order by fc.created asc;'''):
            mapa_json.append({"uv":r.numero_uv,"created": str(r.created)})
        prueba_diccionario = mapa_json






    context = {
        # 'archivo':archivo,
        # 'diccionario':diccionario,
        'filtro_tiempo':filtro_tiempo,
        'prueba_diccionario':prueba_diccionario,
        # 'contador':contador_dir
        

    }

    return render(request,'vis/farmacia_vis.html', context)

def dimap_vis(request):
    uv = UV.objects.all()
    control_de_plaga = ControlPlaga.objects.all()
    seguridad_dimap = SeguridadDIMAP.objects.all()
    esterilizacion = Procedimiento.objects.all()



    context = {
        'uv':uv
    }

    return render(request,'vis/dimap_vis.html', context)

