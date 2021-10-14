from django.db.models import query_utils
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView

import pandas as pd
from django.http import HttpResponse

from .models import *
from .forms import (
    ProductoFarmaciaForm,
    ComprobanteVentaForm,
    ComprobanteVentaModelForm,
    ProductoVendidoForm,
    ProductoVendidoFormset
)
from .filters import (
    ProductoFarmaciaFilter,
    ComprobanteVentaFilter,
)



            #COMPROVANTE VENTA



class InicioComprobanteVenta(ListView):
    model = ComprobanteVenta
    ordering = ['-created']
    context_object_name = 'post'
    paginate_by = 2

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['filter'] = ComprobanteVentaFilter(self.request.GET, queryset=self.get_queryset())
        return context


@login_required
def comprobante_venta_form(request, pk):
    persona = Persona.objects.get(pk=pk)
    formset = ProductoVendidoFormset()
    form = ComprobanteVentaModelForm()
    if request.method == 'POST':
        form = ComprobanteVentaModelForm(request.POST, request.FILES)
        formset = ProductoVendidoFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            obj = form.save(commit=False)
            obj.comprador = persona
            obj.farmaceuta = request.user
            obj.save()
            cv = obj
            for form in formset:
                nombre = form.cleaned_data.get('nombre')
                cantidad = form.cleaned_data.get('cantidad')
                if nombre:
                    ProductoVendido(nombre=nombre,
                                    cantidad=cantidad,
                                    n_venta=cv,
                                    farmaceuta=request.user).save()
            
            return redirect('comprobanteventa-detail',pk=cv)

    context = {
        'c_form': form,
        'persona':persona,
        'formset':formset,
    }

    return render(request, 'farmacia/comprobanteventa_form.html', context)
    
    # persona = Persona.objects.get(pk=pk)
    # c_form = ComprobanteVentaForm()
    # formset = ProductoVendidoFormset()
    

    # if request.method == 'POST':
    #     cv = ComprobanteVenta.objects.create(farmaceuta=request.user,comprador=persona)
    #     # cv.numero_identificacion = persona.numero_identificacion
    #     # cv.tipo_identificacion = persona.tipo_identificacion
    #     print(request.POST.get('receta'))
    #     f = request.POST.get('receta')
    #     cv.receta = request.POST.get('receta')
    #     print(cv.receta)
    #     formset = ProductoVendidoFormset(request.POST)
    #     if formset.is_valid():
    #         print(request.FILES)
    #         # cv.receta = request.FILES
    #         for form in formset:
    #             nombre = form.cleaned_data.get('nombre')
    #             cantidad = form.cleaned_data.get('cantidad')
    #             n_venta = cv
    #             if nombre:
    #                 ProductoVendido(nombre=nombre,
    #                                 cantidad=cantidad,
    #                                 n_venta=n_venta,
    #                                 farmaceuta=request.user).save()
    #         cv.save()
    #         return redirect('comprobanteventa-detail',pk=cv)

    # context = {
    #     'c_form': c_form,
    #     'formset':formset,
    #     'persona':persona,
    # }

    # return render(request, 'farmacia/comprobanteventa_form.html', context)

@login_required
def comprobante_venta_detail(request, pk):
    c_venta = ComprobanteVenta.objects.get(pk=pk)
    p_vendido = ProductoVendido.objects.filter(n_venta=pk)
    persona = c_venta.comprador

    productos = [producto for producto in p_vendido.values()]
    total = calcular_total(p_vendido, productos)
    st = calcular_subtotales(p_vendido, productos)

    context = {
        'c_detail': c_venta,
        'pv_detail': p_vendido,
        'total': total,
        'persona': persona
    }

    return render(request, 'farmacia/comprobanteventa_detail.html', context)


@login_required
def comprobante_venta_edicion(request, pk):
    c_venta = ComprobanteVenta.objects.get(pk=pk)
    p_vendido = ProductoVendido.objects.filter(n_venta=pk)
    persona = c_venta.comprador

    productos = [producto for producto in p_vendido.values()]
    total = calcular_total(p_vendido, productos)
    st = calcular_subtotales(p_vendido, productos)

    context = {
        'c_detail': c_venta,
        'pv_detail': p_vendido,
        'total': total,
        'persona': persona
    }

    return render(request, 'farmacia/comprobanteventa_edicion.html', context)


class EdicionComprobanteVenta(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = ComprobanteVenta    
    form_class = ComprobanteVentaForm
    template_name='farmacia/comprobanteventa_update.html'

    def form_valid(self, form):
        form.instance.farmaceuta = self.request.user
        return super().form_valid(form)

    def test_func(self):
        formulario = self.get_object()
        if self.request.user == formulario.farmaceuta:
            return True
        return False

@login_required
def comprobante_venta_delete(request, pk):
    c_venta = ComprobanteVenta.objects.get(pk=pk)

    if request.method == 'POST':
        if request.user == c_venta.farmaceuta:
            c_venta.delete()
            messages.success(request, f'El comporbante de venta fue eliminado con exito')
            return redirect('comprobanteventa-inicio')
        else:
            messages.warning(request, f'No esta autorizado para eliminar el comprobante de venta')
            return redirect('comprobanteventa-inicio')

    context = {
        'object': c_venta,
    }

    return render(request, 'farmacia/delete.html', context)



            #PRODUCTO VENDIDO




@login_required
def producto_vendido_crear(request, pk):
    
    n_venta = pk
    form = ProductoVendidoForm()
    cv = ComprobanteVenta.objects.get(pk=n_venta)

    if request.method == 'POST':
        form = ProductoVendidoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data.get('nombre')
            cantidad = form.cleaned_data.get('cantidad')
            ProductoVendido(nombre=nombre,
                            cantidad=cantidad,
                            n_venta=cv,
                            farmaceuta=request.user).save()

            messages.success(request, f'El Producto {nombre} fue agregado con exito!!')
            return redirect('comprobanteventa-detail', pk=n_venta)
    else:
        form = ProductoVendidoForm()

    context = {
        'form': form,
    }

    return render(request, 'farmacia/productovendido_nuevo.html', context)

class EdicionProductoVendido(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = ProductoVendido
    form_class = ProductoVendidoForm

    def form_valid(self, form):
        form.instance.farmaceuta = self.request.user
        return super().form_valid(form)

    def test_func(self):
        formulario = self.get_object()
        if self.request.user == formulario.farmaceuta:
            return True
        return False

@login_required
def producto_vendido_delete(request, pk):
    p_vendido = ProductoVendido.objects.get(pk=pk)
    n_venta = p_vendido.n_venta

    if request.method == 'POST':
        if request.user == p_vendido.farmaceuta:
            p_vendido.delete()
            messages.success(request, f'El producto vendido fue eliminado con exito')
            return redirect('comprobanteventa-detail', pk=n_venta)
        else:
            messages.warning(request, f'No esta autorizado para eliminar el producto vendido')
            return redirect('comprobanteventa-inicio')

    context = {
        'object': p_vendido,
    }

    return render(request, 'farmacia/delete.html', context)

@login_required
def producto_vendido_delete_edicion(request, pk):
    p_vendido = ProductoVendido.objects.get(pk=pk)
    n_venta = p_vendido.n_venta

    if request.method == 'POST':
        if request.user == p_vendido.farmaceuta:
            p_vendido.delete()
            messages.success(request, f'El producto vendido fue eliminado con exito')
            return redirect('comprobanteventa-detail', pk=n_venta)
        else:
            messages.warning(request, f'No esta autorizado para eliminar el producto vendido')
            return redirect('comprobanteventa-inicio')

    context = {
        'object': p_vendido,
    }

    return render(request, 'farmacia/delete.html', context)



            #PRODUCTO FARMACIA



class InicioProductoFarmacia(ListView):
    model = ProductoFarmacia
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductoFarmaciaFilter(self.request.GET, queryset=self.get_queryset())
        return context

@login_required
def crear_producto_farmacia(request):
    form = ProductoFarmaciaForm()
    
    if request.method == 'POST':
        form = ProductoFarmaciaForm(request.POST)
        if form.is_valid():
            ProductoFarmacia(autor=request.user,
                            marca_producto=form.cleaned_data.get('marca_producto'),
                            p_a=form.cleaned_data.get('p_a'),
                            dosis=form.cleaned_data.get('dosis'),
                            presentacion =form.cleaned_data.get('presentacion'),
                            f_ven =form.cleaned_data.get('f_ven'),
                            precio=form.cleaned_data.get('precio'),
                            n_lote=form.cleaned_data.get('n_lote')).save()
            messages.success(request, f'El producto fue creado con exito')
            return redirect('productofarmacia-inicio')


    return render(request, 'farmacia/productofarmacia_form.html')

class EdicionProductoFarmacia(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = ProductoFarmacia
    form_class = ProductoFarmaciaForm
    template_name = 'farmacia/productofarmacia_update.html'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        formulario = self.get_object()
        if self.request.user == formulario.autor:
            return True
        return False

@login_required
def producto_farmacia_delete(request, pk):
    producto_farmacia = ProductoFarmacia.objects.get(pk=pk)

    if request.method == 'POST':
        producto_farmacia.delete()
        return redirect('productofarmacia-inicio')

    context = {
        'object': producto_farmacia,
    }

    return render(request, 'farmacia/delete.html', context)



            #FUNCIONALIDADES EXTRAS

def descargar_comprobantes(request):

    df = pd.DataFrame(list(ComprobanteVenta.objects.all().values())).astype(str)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=ComprobantesDeVenta.xlsx'
    df.to_excel(excel_writer=response, index=None)

    return response

def calcular_total(productos_queryset, productos):

    total = 0
    for producto in productos:
        p_farmacia = ProductoFarmacia.objects.get(pk=producto['nombre_id'])
        precio = p_farmacia.precio
        cantidad = producto['cantidad']
        total = total + (precio*cantidad)

    return total

def calcular_subtotales(productos_queryset, productos):

    subtotales = []

    for producto in productos_queryset:        
        precio = ProductoFarmacia.objects.get(pk=producto.nombre_id).precio
        producto.v_unitario = precio
        producto.subtotal = precio*producto.cantidad

    return 0
