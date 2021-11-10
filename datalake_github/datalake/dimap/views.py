from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
)

from core.models import(
    Persona,
    Telefono,
    Correo,
    Direccion,
)

from core.forms import(
    PersonaVerificacionForm,
)

from .models import (
    Procedimiento,
    Mascota,
    ControlPlaga,
)
from .forms import (
    ProcedimientoModelForm,
    MascotaModelForm,
    ControlPlagaModelForm,
)
from .filters import (
    ProcedimientoFilter,
    ControlPlagaFilter,
)

class InicioEsterilizacion(ListView):
    model = Procedimiento
    ordering = ['-created']
    context_object_name = 'post'
    template_name = 'dimap/esterilizacion_inicio.html'

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['filter'] = ProcedimientoFilter(self.request.GET, queryset=self.get_queryset())
        return context

@login_required
def esterilizacion_verificacion_identidad(request):
    
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
                return redirect('esterilizacion-crear', pk=pk)
            else:
                return redirect('persona-crear', pk=2)

    context = {
        'v_persona': verificador_de_personas,
    }

    return render(request, 'dimap/esterilizacion_verificacion.html', context)



@login_required
def esterilizacion_form(request,pk):
    persona = Persona.objects.get(pk=pk)
    telefono = Telefono.objects.get(persona=persona)
    correo = Correo.objects.get(persona=persona)
    direccion = Direccion.objects.get(persona=persona)
    
    form_mascota = MascotaModelForm()
    form_esterilizacion = ProcedimientoModelForm()
    if request.method == 'POST':
        form_mascota = MascotaModelForm(request.POST)
        form_esterilizacion = ProcedimientoModelForm(request.POST)
        if form_esterilizacion.is_valid() and form_mascota.is_valid():
            mascota = form_mascota.save(commit=False)
            esterilizacion = form_esterilizacion.save(commit=False)
            mascota.persona = persona
            mascota.save()
            esterilizacion.autor = request.user
            esterilizacion.mascota = mascota
            esterilizacion.save()
            form_id = esterilizacion.id
            messages.success(request, f'El Formulario fue creado con exito')
            return redirect('esterilizacion-detail',pk=form_id)

    context = {
        'form_esterilizacion':form_esterilizacion,
        'form_mascota':form_mascota,
        'persona':persona,
        'telefono':telefono,
        'correo':correo,
        'direccion':direccion,
    }

    return render(request, 'dimap/esterilizacion_form.html', context)

@login_required
def esterilizacion_detail(request, pk):
    esterilizacion = Procedimiento.objects.get(pk=pk)
    mascota = esterilizacion.mascota
    persona = mascota.persona
    direccion = Direccion.objects.get(persona=persona)  

    context = {
        'esterilizacion':esterilizacion,
        'mascota':mascota,
        'persona':persona,
        'direccion':direccion,
    }

    return render(request, 'dimap/esterilizacion_detalle.html', context)

@login_required
def esterilizacion_delete(request, pk):
    obj = Procedimiento.objects.get(pk=pk)

    if request.method == 'POST':
        if request.user == obj.autor:
            obj.delete()
            messages.success(request, f'El formulario fue eliminado con exito')
            return redirect('esterilizacion-inicio')
        else:
            messages.warning(request, f'No esta autorizado para eliminar el formulario')
            return redirect('esterilizacion-inicio')

    context = {
        'object': obj,
    }

    return render(request, 'dimap/esterilizacion_delete.html', context)




#           CONTROL DE PLAGA



class InicioControlPlaga(ListView):
    model = ControlPlaga
    ordering = ['-created']
    context_object_name = 'post'
    template_name = 'dimap/controldeplaga_inicio.html'

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['filter'] = ControlPlagaFilter(self.request.GET, queryset=self.get_queryset())
        return context

@login_required
def controldeplaga_verificacion_identidad(request):
    
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
                return redirect('controldeplaga-crear', pk=pk)
            else:
                return redirect('persona-crear', pk=3)

    context = {
        'v_persona': verificador_de_personas,
    }

    return render(request, 'dimap/controldeplaga_verificacion.html', context)


@login_required
def controldeplaga_form(request,pk):
    persona = Persona.objects.get(pk=pk)
    telefono = Telefono.objects.get(persona=persona)
    correo = Correo.objects.get(persona=persona)
    direccion = Direccion.objects.get(persona=persona)
    
    form_controldeplaga = ControlPlagaModelForm()

    if request.method == 'POST':
        form_controldeplaga = ControlPlagaModelForm(request.POST)

        if form_controldeplaga.is_valid():
            controldeplaga = form_controldeplaga.save(commit=False)
            controldeplaga.persona = persona
            controldeplaga.autor = request.user
 
            controldeplaga.save()
            form_id = controldeplaga.id
            messages.success(request, f'El Formulario fue creado con exito')
            return redirect('controldeplaga-detail',pk=form_id)

    context = {
        'form_controldeplaga':form_controldeplaga,
        'persona':persona,
        'telefono':telefono,
        'correo':correo,
        'direccion':direccion,
    }

    return render(request, 'dimap/controldeplaga_form.html', context)

@login_required
def controldeplaga_detail(request, pk):
    controldeplaga = ControlPlaga.objects.get(pk=pk)
    persona = controldeplaga.persona
    direccion = Direccion.objects.get(persona=persona)  

    context = {
        'controldeplaga':controldeplaga,
        'persona':persona,
        'direccion':direccion,
    }

    return render(request, 'dimap/controldeplaga_detalle.html', context)

@login_required
def controldeplaga_delete(request, pk):
    obj = ControlPlaga.objects.get(pk=pk)

    if request.method == 'POST':
        if request.user == obj.autor:
            obj.delete()
            messages.success(request, f'El formulario fue eliminado con exito')
            return redirect('controldeplaga-inicio')
        else:
            messages.warning(request, f'No esta autorizado para eliminar el formulario')
            return redirect('controldeplaga-inicio')

    context = {
        'object': obj,
    }

    return render(request, 'dimap/controldeplaga_delete.html', context)