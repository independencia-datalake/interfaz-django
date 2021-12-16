import pandas as pd
from django.shortcuts import render
from .models import(
    VisFarmacia,
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
    uv = UV.objects.all()
    # direccion = Direccion.objects.all()
    # persona = Persona.objects.all()
    # comprobante = ComprobanteVenta.objects.all()

    # contador = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    # contador_dir = {'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'11':0,'12':0,'13':0,'14':0,'15':0,'16':0,'17':0,'18':0,'19':0,'20':0,'21':0,'22':0,'23':0,'24':0,'25':0,'26':0,'27':0}

    # for obj in comprobante:
    #     persona = obj.comprador
    #     direccion = Direccion.objects.get(persona=persona)
    #     unidad_vecinal = direccion.uv
    #     contador[unidad_vecinal.numero_uv] += 1
    #     contador_dir[f"{unidad_vecinal}"] += 1
    
    # vis_farmacia_en_s3 = VisFarmacia.objects.get(id=2)
    # vis_farmacia_con_created = VisFarmacia.objects.get(id=3)
    
    # df_s3 = pd.read_csv(vis_farmacia_en_s3.farmacia_archivo)
    # df_created = pd.read_csv(vis_farmacia_con_created.farmacia_archivo)




    context = {
        'uv':uv,
        # 'direccion':direccion,
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

