from django.shortcuts import render

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
)

def vis(request):
    return render(request,'vis/index.html')

def inicio_vis(request):
    return render(request,'vis/inicio_vis.html')

def farmacia_vis(request):
    uv = UV.objects.all()
    direccion = Direccion.objects.all()
    persona = Persona.objects.all()
    comprobante = ComprobanteVenta.objects.all()

    contador = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    contador_dir = {'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'9':0,'10':0,'11':0,'12':0,'13':0,'14':0,'15':0,'16':0,'17':0,'18':0,'19':0,'20':0,'21':0,'22':0,'23':0,'24':0,'25':0,'26':0,'27':0}

    for obj in comprobante:
        persona = obj.comprador
        direccion = Direccion.objects.get(persona=persona)
        unidad_vecinal = direccion.uv
        contador[unidad_vecinal.numero_uv] += 1
        contador_dir[f"{unidad_vecinal}"] += 1
    

    context = {
        'uv':uv,
        'direccion':direccion,
        'contador':contador_dir
        

    }

    return render(request,'vis/farmacia_vis.html', context)

def dimap_vis(request):
    uv = UV.objects.all()  

    context = {
        'uv':uv
    }

    return render(request,'vis/dimap_vis.html', context)

