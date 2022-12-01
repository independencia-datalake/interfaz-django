from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    UpdateView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin,
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
    SeguridadDIMAP,
)
from .forms import (
    ProcedimientoModelForm,
    MascotaModelForm,
    ControlPlagaModelForm,
    SeguridadDIMAPModelForm,
)
from .filters import (
    ProcedimientoFilter,
    ControlPlagaFilter,
    SeguridadDIMAPFilter,
)

import pandas as pd
from django.http import HttpResponse


#           ESTERILIZACION ( MODELO: MASCOTA Y PROCEDIEMNTO )


class InicioEsterilizacion(ListView):
    model = Procedimiento
    paginate_by = 10
    ordering = ['-created']
    context_object_name = 'filtrados'
    template_name = 'dimap/esterilizacion_inicio.html'

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['filter'] = ProcedimientoFilter(self.request.GET, queryset=self.get_queryset())
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        return ProcedimientoFilter(self.request.GET, queryset=queryset).qs
    def get_paginate_by(self, queryset):

        return self.request.GET.get('paginate_by', self.paginate_by)        

@login_required
def esterilizacion_verificacion_identidad(request):
    
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
                return redirect('esterilizacion-crear', pk=pk)
            else:
                return redirect('persona-crear', pk=2, n_iden=n_iden, ty_iden=tipo_identificacion_ver)

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

@login_required
def esterilizacion_edicion(request,pk):
    pro = Procedimiento.objects.get(pk=pk)
    mascota = pro.mascota
    persona = mascota.persona
    telefono = Telefono.objects.get(persona=persona)
    correo = Correo.objects.get(persona=persona)
    direccion = Direccion.objects.get(persona=persona)
    form_mascota = MascotaModelForm(instance=mascota)
    form_esterilizacion = ProcedimientoModelForm(instance=pro)

    if request.method == 'POST':
        form_mascota = MascotaModelForm(
            request.POST,
            instance=mascota,
            )
        form_esterilizacion = ProcedimientoModelForm(
            request.POST,
            instance=pro,
            )
        if form_mascota.is_valid() and form_esterilizacion.is_valid():
            form_mascota.save()
            form_esterilizacion.save()
            messages.success(request, f'El procedimiento se ha actualizado')
            return redirect('esterilizacion-inicio')

    context = {
        'form_mascota':form_mascota,
        'form_esterilizacion':form_esterilizacion,
        'persona':persona,
        'telefono':telefono,
        'correo':correo,
        'direccion':direccion,
    }

    return render(request,'dimap/esterilizacion_edicion.html', context)


#           CONTROL DE PLAGA ( MODELO: CONTROL DE PLAGA )


class InicioControlPlaga(ListView):                 # CLASE QUE MUESTRA EL INICIO DE CONTROL DE PLAGA
    model = ControlPlaga
    ordering = ['-created']
    context_object_name = 'filtrados'
    paginate_by = 10
    template_name = 'dimap/controldeplaga_inicio.html'

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['filter'] = ControlPlagaFilter(self.request.GET, queryset=self.get_queryset())
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        return ControlPlagaFilter(self.request.GET, queryset=queryset).qs
    def get_paginate_by(self, queryset):

        return self.request.GET.get('paginate_by', self.paginate_by)

@login_required
def controldeplaga_verificacion_identidad(request): # FUNCION PARA VERIFICAR LA IDENTIDAD CONTROL DE PLAGA
    
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
                return redirect('controldeplaga-crear', pk=pk)
            else:
                return redirect('persona-crear', pk=3, n_iden=n_iden, ty_iden=tipo_identificacion_ver)

    context = {
        'v_persona': verificador_de_personas,
    }

    return render(request, 'dimap/controldeplaga_verificacion.html', context)

@login_required
def controldeplaga_form(request,pk):                # FUNCION PARA LA CREACION DE UN NUEVO FORMULARIO
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
def controldeplaga_detail(request, pk):             # FUNCION QUE MUESTRA EL DETALLE DEL FORMULARIO (COMPROBAR FORMULARIO)
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
def controldeplaga_delete(request, pk):             # FUNCION PARA ELIMINAR CONTROL DE PLAGA
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

class EdicionControlPlaga(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = ControlPlaga
    form_class = ControlPlagaModelForm
    template_name = 'dimap/controldeplaga_edicion.html'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        formulario = self.get_object()
        if self.request.user == formulario.autor:
            return True
        return False



    #           SEGURIDAD DIMAP


#           SEGURIDAD DIMAP ( MODELO: SEGURIDAD DIMAP )


class InicioSeguridadDIMAP(ListView):
    model = SeguridadDIMAP
    ordering = ['-created']
    context_object_name = 'filtrados'
    paginate_by = 10
    template_name = 'dimap/seguridad_inicio.html'

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['filter'] = SeguridadDIMAPFilter(self.request.GET, queryset=self.get_queryset())
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        return SeguridadDIMAPFilter(self.request.GET, queryset=queryset).qs
    def get_paginate_by(self, queryset):

        return self.request.GET.get('paginate_by', self.paginate_by)

@login_required
def seguridad_verificacion_identidad(request):
    
    verificador_de_personas = PersonaVerificacionForm()

    if request.method == 'POST':
        verificador_de_personas = PersonaVerificacionForm(request.POST)
        if verificador_de_personas.is_valid():
            tipo_identificacion_ver = verificador_de_personas.cleaned_data.get('tipo_identificacion')
            numero_identificacion_ver = verificador_de_personas.cleaned_data.get('numero_identificacion')
            n_iden = numero_identificacion_ver
            if tipo_identificacion_ver == "RUT": # INCLUYE PUNTOS Y GIONES AL RUT
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
            persona_buscada = Persona.objects.filter(numero_identificacion=numero_identificacion_ver) # BUSCA PERSONA SI ES QUE EXISTE
            if persona_buscada:
                pk = persona_buscada[0].id
                return redirect('seguridad-crear', pk=pk)
            else:
                return redirect('persona-crear', pk=4, n_iden=n_iden, ty_iden=tipo_identificacion_ver) # LA PK DEFINE DESDE QUE FORMULARIO SE REQUERE LA VERIFICACION DE PERSONA

    context = {
        'v_persona': verificador_de_personas,
    }

    return render(request, 'dimap/seguridad_verificacion.html', context)

@login_required
def seguridad_form(request,pk):
    persona = Persona.objects.get(pk=pk)
    telefono = Telefono.objects.get(persona=persona)
    correo = Correo.objects.get(persona=persona)
    direccion = Direccion.objects.get(persona=persona)
    
    form_seguridad = SeguridadDIMAPModelForm()

    if request.method == 'POST':
        form_seguridad = SeguridadDIMAPModelForm(request.POST, request.FILES)

        if form_seguridad.is_valid():
            seguridad = form_seguridad.save(commit=False)
            seguridad.persona = persona
            seguridad.autor = request.user
 
            seguridad.save()
            form_id = seguridad.id
            messages.success(request, f'El Formulario fue creado con exito')
            return redirect('seguridad-detail',pk=form_id)

    context = {
        'form_seguridad':form_seguridad,
        'persona':persona,
        'telefono':telefono,
        'correo':correo,
        'direccion':direccion,
    }

    return render(request, 'dimap/seguridad_form.html', context)

@login_required
def seguridad_detail(request, pk):
    seguridad = SeguridadDIMAP.objects.get(pk=pk)
    persona = seguridad.persona
    direccion = Direccion.objects.get(persona=persona)  

    context = {
        'seguridad':seguridad,
        'persona':persona,
        'direccion':direccion,
    }

    return render(request, 'dimap/seguridad_detalle.html', context)

@login_required
def seguridad_delete(request, pk):
    obj = SeguridadDIMAP.objects.get(pk=pk)

    if request.method == 'POST':
        if request.user == obj.autor:
            obj.delete()
            messages.success(request, f'El formulario fue eliminado con exito')
            return redirect('seguridad-inicio')
        else:
            messages.warning(request, f'No esta autorizado para eliminar el formulario')
            return redirect('seguridad-inicio')

    context = {
        'object': obj,
    }

    return render(request, 'dimap/seguridad_delete.html', context)

class EdicionSeguridadDIMAP(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = SeguridadDIMAP
    form_class = SeguridadDIMAPModelForm
    template_name = 'dimap/seguridad_edicion.html'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        formulario = self.get_object()
        if self.request.user == formulario.autor:
            return True
        return False


@login_required
def descargar_control_plaga(request):

    df = pd.DataFrame(list(ControlPlaga.objects.all().values())).astype(str)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=control_de_plaga.xlsx'
    df.to_excel(excel_writer=response, index=None)

    return response

@login_required
def descargar_esterilizacion(request):

    df = pd.DataFrame(list(Procedimiento.objects.all().values())).astype(str)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=procedimiento_esterilizacion.xlsx'
    df.to_excel(excel_writer=response, index=None)

    return response

@login_required
def descargar_seguridad_dimap(request):

    df = pd.DataFrame(list(SeguridadDIMAP.objects.all().values())).astype(str)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=seguridad_DIMAP.xlsx'
    df.to_excel(excel_writer=response, index=None)

    return response