from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import(
    CargaEntregaPandemiaForm,
    CargaEmpresasForm,
    CargaPatentesVehicularesForm,
    CargaPermisosCirculacionForm,
    CargaExencionAseoForm,
    CargaDOMForm,
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