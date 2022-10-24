from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
)
from .models import(
    ClasificacionDelito,
    Delito,
    Requerimiento,
    LlamadoSeguridad,
)
from .filters import(
    RequerimientoFilter,
)
from .forms import(
    DenuncianteModelForm,
    RequerimientoInicioModelForm,
    RequerimientoDelitoModelForm,
    RequerimientoUbicacionModelForm,
    RequerimientoResolucionModelForm,
)

import pandas as pd
from django.http import HttpResponse


class InicioRequerimineto(ListView):
    model = Requerimiento
    ordering = ['-created']
    context_object_name = 'post'
    template_name = 'seguridad/denuncia_inicio.html'

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['filter'] = RequerimientoFilter(self.request.GET, queryset=self.get_queryset())
        return context

@login_required
def requerimiento_form(request, nr):
    llamado = None
    if nr == 0:
        form_req_inicio = RequerimientoInicioModelForm()
        form_req_delito = RequerimientoDelitoModelForm()
        form_denunciante = DenuncianteModelForm()
        form_req_ubicacion = RequerimientoUbicacionModelForm()
        form_req_resolucion = RequerimientoResolucionModelForm()
    else:
        llamado = LlamadoSeguridad.objects.get(pk=nr)
        requerimientos = Requerimiento.objects.filter(numero_requerimiento=nr)
        requerimiento = requerimientos[0]
        denunciante = requerimiento.denunciante

        form_req_inicio = RequerimientoInicioModelForm(instance=requerimiento)
        form_req_delito = RequerimientoDelitoModelForm()
        form_denunciante = DenuncianteModelForm(instance=denunciante)
        form_req_ubicacion = RequerimientoUbicacionModelForm(instance=requerimiento)
        form_req_resolucion = RequerimientoResolucionModelForm(instance=requerimiento)

    # CREACION DEL RADIO SELECT PARA EL FORMULARIO

    clasificacion_delito = ClasificacionDelito.objects.all()
    diccionario = {}
    for cla in clasificacion_delito:
        lista_delito = []
        delitos = Delito.objects.filter(clasificacion_delito=cla.id)
        for delito in delitos:
            delito_obj = {
                'nombre':delito.nombre,
                'id':int(delito.id),
                'n':int(delito.id)-1,
            }
            lista_delito.append(delito_obj)
        diccionario[cla.nombre] = lista_delito

    if request.method == 'POST':
        if llamado == None:
            numero_requerimiento = LlamadoSeguridad.objects.create()
            nr = numero_requerimiento.numero_requerimiento
            form_req_inicio = RequerimientoInicioModelForm(request.POST)
            form_req_delito = RequerimientoDelitoModelForm(request.POST)
            form_denunciante = DenuncianteModelForm(request.POST)
            form_req_ubicacion = RequerimientoUbicacionModelForm(request.POST)
            form_req_resolucion = RequerimientoResolucionModelForm(request.POST)
        else:
            nr = llamado.numero_requerimiento
            form_req_inicio = RequerimientoInicioModelForm(request.POST, instance=requerimiento)
            form_req_delito = RequerimientoDelitoModelForm(request.POST)
            form_denunciante = DenuncianteModelForm(request.POST, instance=denunciante)
            form_req_ubicacion = RequerimientoUbicacionModelForm(request.POST, instance=requerimiento)
            form_req_resolucion = RequerimientoResolucionModelForm(request.POST, instance=requerimiento)

        if form_denunciante.is_valid() and form_req_inicio.is_valid() and form_req_ubicacion.is_valid() and form_req_resolucion.is_valid() and form_req_delito.is_valid():
            if llamado == None:
                denunciante = form_denunciante.save()
                obj = Requerimiento.objects.create(
                    numero_requerimiento = numero_requerimiento , #numero de requerimento
                    estatus= form_req_inicio.cleaned_data.get('estatus'),      ## FORMULARIO INICIO
                    via_ingreso=form_req_inicio.cleaned_data.get('via_ingreso'), ## FORMULARIO INICIO
                    via_ingreso_otro=form_req_inicio.cleaned_data.get('via_ingreso_otro'), ## FORMULARIO INICIO
                    denunciante= denunciante ,                                  # DENUNCIANTE AGREEGAR ANONIMO
                    delito=form_req_delito.cleaned_data.get('delito'),          #DELITO 
                    delito_otro=form_req_delito.cleaned_data.get('delito_otro'), #DELITO 
                    calle = form_req_ubicacion.cleaned_data.get('calle'),       #FORMULARIO UBICACION
                    numero = form_req_ubicacion.cleaned_data.get('numero'),        #FORMULARIO UBICACION
                    complemento_direccion=form_req_ubicacion.cleaned_data.get('complemento_direccion'), #FORMULARIO UBICACION 
                    interseccion=form_req_ubicacion.cleaned_data.get('interseccion'), #FORMULARIO UBICACION 
                    prioridad=form_req_resolucion.cleaned_data.get('prioridad'), #FORMULARIO RESOLUCION 
                    resolucion=form_req_resolucion.cleaned_data.get('resolucion'),  #FORMULARIO RESOLUCION 
                    resolucion_otro=form_req_resolucion.cleaned_data.get('resolucion_otro'), #FORMULARIO RESOLUCION 
                    autor=request.user,
                )
                obj_id = obj.numero_requerimiento
            else:
                obj = Requerimiento.objects.create(
                    numero_requerimiento = llamado , #numero de requerimento
                    estatus= form_req_inicio.cleaned_data.get('estatus'),      ## FORMULARIO INICIO
                    via_ingreso=form_req_inicio.cleaned_data.get('via_ingreso'), ## FORMULARIO INICIO
                    via_ingreso_otro=form_req_inicio.cleaned_data.get('via_ingreso_otro'), ## FORMULARIO INICIO
                    denunciante= denunciante ,                                  # DENUNCIANTE AGREEGAR ANONIMO
                    delito=form_req_delito.cleaned_data.get('delito'),          #DELITO 
                    delito_otro=form_req_delito.cleaned_data.get('delito_otro'), #DELITO 
                    calle = form_req_ubicacion.cleaned_data.get('calle'),       #FORMULARIO UBICACION
                    numero = form_req_ubicacion.cleaned_data.get('numero'),        #FORMULARIO UBICACION
                    complemento_direccion=form_req_ubicacion.cleaned_data.get('complemento_direccion'), #FORMULARIO UBICACION 
                    interseccion=form_req_ubicacion.cleaned_data.get('interseccion'), #FORMULARIO UBICACION 
                    prioridad=form_req_resolucion.cleaned_data.get('prioridad'), #FORMULARIO RESOLUCION 
                    resolucion=form_req_resolucion.cleaned_data.get('resolucion'),  #FORMULARIO RESOLUCION 
                    resolucion_otro=form_req_resolucion.cleaned_data.get('resolucion_otro'), #FORMULARIO RESOLUCION 
                    autor=request.user,
                )
                obj_id = obj.numero_requerimiento
            
            messages.success(request, f'La denuncia fue creada con exito')
            return redirect('denuncia-detalle',pk=obj_id)

    context = {
        'form_req_inicio':form_req_inicio,
        'form_req_delito':form_req_delito,
        'form_denunciante':form_denunciante,
        'form_req_ubicacion':form_req_ubicacion,
        'form_req_resolucion':form_req_resolucion,
        'diccionario':diccionario,
    }

    return render(request,'seguridad/denuncia_form.html', context)
    
@login_required
def requermineto_detalle(request,pk):
    llamado = LlamadoSeguridad.objects.get(pk=pk)
    requerimientos = Requerimiento.objects.filter(numero_requerimiento=pk)
    datos_compartidos = requerimientos[0]

    context = {
        'llamado':llamado,
        'datos_compartidos':datos_compartidos,
        'requerimientos': requerimientos,
    }

    return render(request, 'seguridad/denuncia_detalle.html', context)

@login_required
def requermineto_delete(request, pk):
    obj = Requerimiento.objects.get(pk=pk)

    if request.method == 'POST':
        if request.user == obj.autor:
            obj.delete()
            messages.success(request, f'La denuncia fue eliminada con exito')
            return redirect('denuncia-inicio')
        else:
            messages.warning(request, f'No esta autorizado para eliminar el formulario')
            return redirect('denuncia-inicio')

    context = {
        'object': obj,
    }

    return render(request, 'seguridad/denuncia_delete.html', context)

@login_required
def requermineto_edicion(request, pk):
    requerimiento = Requerimiento.objects.get(pk=pk)
    denunciante = requerimiento.denunciante
    numero_requerimiento = requerimiento.numero_requerimiento

    clasificacion_delito = ClasificacionDelito.objects.all()
    diccionario = {}
    for cla in clasificacion_delito:
        lista_delito = []
        delitos = Delito.objects.filter(clasificacion_delito=cla.id)
        for delito in delitos:
            checked = None
            if delito == requerimiento.delito:
                checked = 'checked'
            delito_obj = {
                'nombre':delito.nombre,
                'id':int(delito.id),
                'n':int(delito.id)-1,
                'checked':checked
            }
            lista_delito.append(delito_obj)
        diccionario[cla.nombre] = lista_delito
    form_req_inicio = RequerimientoInicioModelForm(instance=requerimiento)
    form_req_delito = RequerimientoDelitoModelForm(instance=requerimiento)
    form_denunciante = DenuncianteModelForm(instance=denunciante)
    form_req_ubicacion = RequerimientoUbicacionModelForm(instance=requerimiento)
    form_req_resolucion = RequerimientoResolucionModelForm(instance=requerimiento)

    if request.method == 'POST':
        form_req_inicio = RequerimientoInicioModelForm(request.POST, instance=requerimiento)
        form_req_delito = RequerimientoDelitoModelForm(request.POST, instance=requerimiento)
        form_denunciante = DenuncianteModelForm(request.POST, instance=denunciante)
        form_req_ubicacion = RequerimientoUbicacionModelForm(request.POST, instance=requerimiento)
        form_req_resolucion = RequerimientoResolucionModelForm(request.POST, instance=requerimiento)
        if form_denunciante.is_valid() and form_req_inicio.is_valid() and form_req_ubicacion.is_valid() and form_req_resolucion.is_valid() and form_req_delito.is_valid():
            form_req_inicio.save(),
            form_req_delito.save(),
            form_denunciante.save(),
            form_req_ubicacion.save(),
            form_req_resolucion.save(),
            messages.success(request, f'La denuncia fue actualizada con exito')

            return redirect('denuncia-detalle', numero_requerimiento)
        

    context = {
        'form_req_inicio':form_req_inicio,
        'form_req_delito':form_req_delito,
        'form_denunciante':form_denunciante,
        'form_req_ubicacion':form_req_ubicacion,
        'form_req_resolucion':form_req_resolucion,
        'diccionario':diccionario,

    }

    return render(request, 'seguridad/denuncia_form.html', context)

# Manejador de descarga
@login_required
def descargar_requerimiento_seguridad(request):

    df = pd.DataFrame(list(Requerimiento.objects.all().values())).astype(str)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=requerimiento_seguridad.xlsx'
    df.to_excel(excel_writer=response, index=None)

    return response