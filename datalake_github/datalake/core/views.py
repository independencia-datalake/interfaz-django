from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import (
    Persona,
    CallesIndependencia,
)
from .forms import (
    PersonaForm,
    PersonaVerificacionForm
)

# AUTOCOMPLETADO CALLES

from django.http import JsonResponse

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
            else:
                return redirect('persona-crear')

    context = {
        'v_persona': verificador_de_personas,
    }

    return render(request, 'core/persona.html', context)

    
    
    #FORMULARIO DE CREACION DE PERSONA

@login_required
def persona_crear(request):
    persona = PersonaForm()

    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            # INCLUYE PUNTOS Y GIONES AL RUT
            tipo_identificacion_ver = form.cleaned_data.get('tipo_identificacion')
            numero_identificacion_ver = form.cleaned_data.get('numero_identificacion')
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
            form.save()
            messages.success(request, f'La persona fue creado con exito')
            persona_buscada = Persona.objects.get(numero_identificacion=numero_identificacion_ver)
            pk = persona_buscada.id
            return redirect('comprobanteventa-create', pk=pk)

    context = {
        'persona': persona,
    }

    return render(request, 'core/persona_form.html', context)



