from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import (
    Persona,
    CallesIndependencia,
    Direccion,
)
from .forms import (
    PersonaModelForm,
    PersonaVerificacionForm,
    TelefonoModelForm,
    CorreoModelForm,
    DireccionModelForm,
)

@login_required
def inicio(request):
    return render(request, 'core/home.html')

    #ENTRADA A PREGUNTA USUARIO
@login_required
def persona(request):
    verificador_de_personas = PersonaVerificacionForm()

    if request.method == 'POST':
        verificador_de_personas = PersonaVerificacionForm(request.POST)
        if verificador_de_personas.is_valid():
            # INCLUYE PUNTOS Y GIONES AL RUT
            tipo_identificacion_ver = verificador_de_personas.cleaned_data.get('tipo_identificacion')
            numero_identificacion_ver = verificador_de_personas.cleaned_data.get('numero_identificacion')
            n_iden = numero_identificacion_ver
            if tipo_identificacion_ver == "RUT":
                ni = numero_identificacion_ver
                if len(ni)==0:
                    None
                elif len(ni)>10:
                    rut = ni[:-10]+'.'+ni[-10:-7]+'.'+ni[-7:-4]+'.'+ni[-4:-1]+'-'+ni[-1]
                    numero_identificacion_ver = rut  
                elif len(ni)==9:
                    rut = ni[-10:-7]+'.'+ni[-7:-4]+'.'+ni[-4:-1]+'-'+ni[-1]
                    numero_identificacion_ver = rut  
                else:
                    rut = ni[-9:-7]+'.'+ni[-7:-4]+'.'+ni[-4:-1]+'-'+ni[-1]
                    numero_identificacion_ver = rut  
            # BUSCA PERSONA SI ES QUE EXISTE
            persona_buscada = Persona.objects.filter(numero_identificacion=numero_identificacion_ver)
            if persona_buscada:
                pk = persona_buscada[0].id
                return redirect('comprobanteventa-create', pk=pk)
            # else:
            #     return redirect('persona-crear',pk=1)
            else:
                return redirect('persona-crear',pk=1,n_iden=n_iden, ty_iden=tipo_identificacion_ver)

    context = {
        'v_persona': verificador_de_personas,
    }

    return render(request, 'core/persona.html', context)

@login_required
def persona_crear(request, pk, n_iden,ty_iden):
    ruta = pk
    persona = PersonaModelForm(initial={
        'numero_identificacion': n_iden,
        'tipo_identificacion':ty_iden,
        })
    telefono = TelefonoModelForm()
    correo = CorreoModelForm()
    direccion = DireccionModelForm()

    if request.method == 'POST':
        form_persona = PersonaModelForm(request.POST)
        form_telefono = TelefonoModelForm(request.POST)
        form_correo = CorreoModelForm(request.POST)
        form_direccion = DireccionModelForm(request.POST)
        forms = [
            form_telefono,
            form_correo,
            form_direccion,
            ]
        if form_persona.is_valid() and form_telefono.is_valid() and form_correo.is_valid() and form_direccion.is_valid():
            persona = form_persona.save(commit=False)
            persona.save()
            pk = persona.id
            for form in forms:
                obj = form.save(commit=False)
                obj.persona = persona
                obj.save()
            # persona.save()
            direccion_nueva = Direccion.objects.get(persona=pk)
            uv_nueva = direccion_nueva.uv
            persona.uv = uv_nueva
            persona.save()
            messages.success(request, f'La persona fue creado con exito')
            if ruta == 1:
                return redirect('comprobanteventa-create', pk=pk)
            elif ruta == 2:
                return redirect('esterilizacion-crear', pk=pk)
            elif ruta == 3:
                return redirect('controldeplaga-crear', pk=pk)
            elif ruta == 4:
                return redirect('seguridad-crear', pk=pk)
            else:
                return redirect('core-home')

    context = {
        'persona': persona,
        'telefono':telefono,
        'correo':correo,
        'direccion':direccion,
    }

    return render(request, 'core/persona_form.html', context)

