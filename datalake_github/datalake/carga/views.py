from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pandas as pd
from django.http import HttpResponse
from .forms import(
    CargaEntregaPandemiaForm,
    CargaEmpresasForm,
    CargaPatentesVehicularesForm,
    CargaPermisosCirculacionForm,
    CargaExencionAseoForm,
    CargaDOMForm,
)
from .models import (
    Empresas,
    PermisosCirculacion,
    PatentesVehiculares,
    EntregasPandemia,
    DOM,
    ExencionAseo
)


@login_required
def carga_datos_entrega_pandemia(request):
    carga_form = CargaEntregaPandemiaForm()

    if request.method == 'POST':
        carga_form = CargaEntregaPandemiaForm(request.POST,request.FILES)
        if carga_form.is_valid():
            carga_form.save()
            messages.success(request, f'El archivo fue subido con exito')
            return redirect('carga-home')
        
    context = {
        'datos':carga_form
    }

    return render(request, 'carga/carga_ayuda_pandemia.html', context)

@login_required
def carga_datos_empresa(request):
    carga_form = CargaEmpresasForm()

    if request.method == 'POST':
        carga_form = CargaEmpresasForm(request.POST,request.FILES)
        if carga_form.is_valid():
            carga_form.save()
            messages.success(request, f'El archivo fue subido con exito')
            return redirect('carga-home')
        
    context = {
        'datos':carga_form
    }

    return render(request, 'carga/carga_empresas.html', context)      

@login_required
def carga_datos_patentes_vehiculares(request):
    carga_form = CargaPatentesVehicularesForm()

    if request.method == 'POST':
        carga_form = CargaPatentesVehicularesForm(request.POST,request.FILES)
        if carga_form.is_valid():
            carga_form.save()
            messages.success(request, f'El archivo fue subido con exito')
            return redirect('carga-home')
        
    context = {
        'datos':carga_form
    }

    return render(request, 'carga/carga_patentes_vehiculares.html', context)   

@login_required
def carga_datos_permiso_circulacion(request):
    carga_form = CargaPermisosCirculacionForm()

    if request.method == 'POST':
        carga_form = CargaPermisosCirculacionForm(request.POST,request.FILES)
        if carga_form.is_valid():
            carga_form.save()
            messages.success(request, f'El archivo fue subido con exito')
            return redirect('carga-home')
        
    context = {
        'datos':carga_form
    }

    return render(request, 'carga/carga_permiso_circulacion.html', context)

@login_required
def carga_datos_exencion_aseo(request):
    carga_form = CargaExencionAseoForm()

    if request.method == 'POST':
        carga_form = CargaExencionAseoForm(request.POST,request.FILES)
        if carga_form.is_valid():
            carga_form.save()
            messages.success(request, f'El archivo fue subido con exito')
            return redirect('carga-home')
        
    context = {
        'datos':carga_form
    }

    return render(request, 'carga/carga_exencion_aseo.html', context)

@login_required
def carga_datos_dom(request):
    carga_form = CargaDOMForm()

    if request.method == 'POST':
        carga_form = CargaDOMForm(request.POST,request.FILES)
        if carga_form.is_valid():
            carga_form.save()
            messages.success(request, f'El archivo fue subido con exito')
            return redirect('carga-home')
        
    context = {
        'datos':carga_form
    }

    return render(request, 'carga/carga_dom.html', context)

@login_required
def descargar_ejemplo_entrega_pandemia(request):

    df = pd.DataFrame(list(EntregasPandemia.objects.filter(pk=1).values())).astype(str)
    del df['id']
    column_names = df.columns
    df_vacia = pd.DataFrame(columns = column_names)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=carga_entregaspandemia.xlsx'
    df_vacia.to_excel(excel_writer=response, index=None)

    return response

@login_required
def descargar_ejemplo_empresa(request):
    df = pd.DataFrame(list(Empresas.objects.filter(pk=1).values())).astype(str)
    del df['id']
    column_names = df.columns
    df_vacia = pd.DataFrame(columns = column_names)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=carga_empresas.xlsx'
    df_vacia.to_excel(excel_writer=response, index=None)

    return response

@login_required
def descargar_ejemplo_patentes_vehiculares(request):
    df = pd.DataFrame(list(PatentesVehiculares.objects.filter(pk=1).values())).astype(str)
    del df['id']
    column_names = df.columns
    df_vacia = pd.DataFrame(columns = column_names)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=carga_patentesvehiculares.xlsx'
    df_vacia.to_excel(excel_writer=response, index=None)

    return response

@login_required
def descargar_ejemplo_permiso_circulacion(request):
    df = pd.DataFrame(list(PermisosCirculacion.objects.filter(pk=1).values())).astype(str)
    del df['id']
    column_names = df.columns
    df_vacia = pd.DataFrame(columns = column_names)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=carga_permisoscirculacion.xlsx'
    df_vacia.to_excel(excel_writer=response, index=None)

    return response

@login_required
def descargar_ejemplo_exencion_aseo(request):
    df = pd.DataFrame(list(ExencionAseo.objects.filter(pk=1).values())).astype(str)
    del df['id']
    column_names = df.columns
    df_vacia = pd.DataFrame(columns = column_names)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=carga_exencionaseo.xlsx'
    df_vacia.to_excel(excel_writer=response, index=None)

    return response

@login_required
def descargar_ejemplo_dom(request):
    df = pd.DataFrame(list(DOM.objects.filter(pk=1).values())).astype(str)
    del df['id']
    column_names = df.columns
    df_vacia = pd.DataFrame(columns = column_names)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=carga_dom.xlsx'
    df_vacia.to_excel(excel_writer=response, index=None)

    return response