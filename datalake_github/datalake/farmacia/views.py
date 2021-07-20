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
from .forms import *
from .filters import (
    ProductoFarmaciaFilter,
    ComprobanteVentaFilter,
)


#VENTA
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
def comprobante_venta_form(request):

    c_form = ComprobanteVentaForm()
    formset = ProductoVendidoFormset()


    if request.method == 'POST':
        cv = ComprobanteVenta.objects.create(farmaceuta=request.user)
        cv.numero_identificacion = request.POST.get('numero_identificacion')
        cv.tipo_identificacion = request.POST.get('tipo_identificacion')
        formset = ProductoVendidoFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                nombre = form.cleaned_data.get('nombre')
                cantidad = form.cleaned_data.get('cantidad')
                n_venta = cv
                if nombre:
                    ProductoVendido(nombre=nombre,
                                    cantidad=cantidad,
                                    n_venta=n_venta,
                                    farmaceuta=request.user).save()
            cv.save()
            messages.success(request, f'El comporbante de venta fue creado con exito')
            return redirect('comprobanteventa-detail',pk=cv)

    context = {
        'c_form': c_form,
        'formset': formset
    }

    return render(request, 'farmacia/comprobanteventa_form.html', context)

@login_required
def comprobante_venta_detail(request, pk):
    c_venta = ComprobanteVenta.objects.get(pk=pk)
    p_vendido = ProductoVendido.objects.filter(n_venta=pk)

    context = {
        'c_detail': c_venta,
        'pv_detail': p_vendido
    }

    return render(request, 'farmacia/comprobanteventa_detail.html', context)

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
        c_venta.delete()
        return redirect('comprobanteventa-inicio')

    context = {
        'object': c_venta,
    }

    return render(request, 'farmacia/delete.html', context)

#PRODUCTO VENDIDO
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

#PRODUCTO FARMACIA
class InicioProductoFarmacia(ListView):
    model = ProductoFarmacia
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductoFarmaciaFilter(self.request.GET, queryset=self.get_queryset())
        return context

class DetalleProductoFarmacia(LoginRequiredMixin, DetailView):
    model = ProductoFarmacia
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class CrearProductoFarmacia(LoginRequiredMixin, CreateView):
    model = ProductoFarmacia
    form_class = ProductoFarmaciaForm

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class EdicionProductoFarmacia(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = ProductoFarmacia
    form_class = ProductoFarmaciaForm

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


def descargar_comprobantes(request):

    df = pd.DataFrame(list(ComprobanteVenta.objects.all().values())).astype(str)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=ComprobantesDeVenta.xlsx'
    df.to_excel(excel_writer=response, index=None)

    return response