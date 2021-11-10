from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import (
    Persona,
    CallesIndependencia,
)
from .forms import (
    PersonaModelForm,
    PersonaVerificacionForm,
    TelefonoModelForm,
    CorreoModelForm,
    DireccionModelForm,
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
                return redirect('persona-crear',pk=1)

    context = {
        'v_persona': verificador_de_personas,
    }

    return render(request, 'core/persona.html', context)

    
    
    #FORMULARIO DE CREACION DE PERSONA

@login_required
def persona_crear(request, pk):
    ruta = pk
    persona = PersonaModelForm()
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
            form_direccion
            ]
        if form_persona.is_valid() and form_telefono.is_valid() and form_correo.is_valid() and form_direccion.is_valid():
            persona = form_persona.save(commit=False)
            persona.save()
            pk = persona.id
            for form in forms:
                obj = form.save(commit=False)
                obj.persona = persona
                obj.save()
            messages.success(request, f'La persona fue creado con exito')
            if ruta == 1:
                return redirect('comprobanteventa-create', pk=pk)
            elif ruta == 2:
                return redirect('esterilizacion-crear', pk=pk)
            elif ruta == 3:
                return redirect('controldeplaga-crear', pk=pk)
            else:
                return redirect('comprobanteventa-create', pk=pk)

    context = {
        'persona': persona,
        'telefono':telefono,
        'correo':correo,
        'direccion':direccion,
    }

    return render(request, 'core/persona_form.html', context)



