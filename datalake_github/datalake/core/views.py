from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from ayuda_funciones.rut import calculadora_rut

from .models import (
    Persona,
    CallesIndependencia,
    Direccion,
    PersonaInfoSalud,
    PersonaArchivos
)
from .forms import (
    PersonaModelForm,
    PersonaVerificacionForm,
    TelefonoModelForm,
    CorreoModelForm,
    DireccionModelForm,
    PersonaInfoSaludModelForm,
    PersonaArchivosModelForm
)

@login_required
def inicio(request):
    if request.user.groups.filter(name='farmacia').exists():
        return redirect('farmacia-home')
    elif request.user.groups.filter(name='dimap').exists():
        return redirect('dimap-home')
    elif request.user.groups.filter(name='seguridad').exists():
        return redirect('seguridad-home')
    else:
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
            numero_identificacion = verificador_de_personas.cleaned_data.get('numero_identificacion')
            if tipo_identificacion_ver == "RUT":
                numero_identificacion_ver = calculadora_rut(numero_identificacion)
            else:
                numero_identificacion_ver = numero_identificacion
            # BUSCA PERSONA SI ES QUE EXISTE
            try:
                persona_buscada = Persona.objects.get(numero_identificacion=numero_identificacion_ver)
            except:
                persona_buscada = False
            if persona_buscada:
                pk = persona_buscada.id
                return redirect('comprobanteventa-create', pk=pk)
            else:
                return redirect('persona-crear',pk=1,n_iden=numero_identificacion_ver, ty_iden=tipo_identificacion_ver)

    context = {
        'v_persona': verificador_de_personas,
    }

    return render(request, 'core/persona.html', context)

@login_required
def persona_crear(request, pk, n_iden,ty_iden):
    ruta = pk
    form_persona = PersonaModelForm(initial={ #anteriormente persona
        'numero_identificacion': n_iden,
        'tipo_identificacion':ty_iden,
        })
    telefono = TelefonoModelForm()
    correo = CorreoModelForm()
    direccion = DireccionModelForm()
    info_salud = PersonaInfoSaludModelForm()
    archivos = PersonaArchivosModelForm()

    if request.method == 'POST':
        form_persona = PersonaModelForm(request.POST)
        telefono = TelefonoModelForm(request.POST) #anteriormente form_telefono
        correo = CorreoModelForm(request.POST) #anteriormente form_correo
        direccion = DireccionModelForm(request.POST) #anteriormente form_direccion
        info_salud = PersonaInfoSaludModelForm(request.POST)  # anteriormente form_info_salud
        archivos = PersonaArchivosModelForm(request.POST, request.FILES)
        files = request.FILES.getlist("file[]")
        forms = [
            telefono, #anteriormente form_telefono
            correo, #anteriormente form_persona
            direccion, #anteriormente form_direccion
            info_salud, # anteriormente form_info_salud
            ]
        if form_persona.is_valid() and telefono.is_valid() and correo.is_valid() and direccion.is_valid() and info_salud.is_valid():
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

            for f in files:
                print(str(f))
                PersonaArchivos(archivo = f,
                persona = persona).save()

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
        'persona': form_persona,
        'telefono':telefono,
        'correo':correo,
        'direccion':direccion,
        'info_salud':info_salud,
        'archivos':archivos,
    }

    return render(request, 'core/persona_form.html', context)

