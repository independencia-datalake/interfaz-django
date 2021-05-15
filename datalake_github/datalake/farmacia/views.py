from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from .models import *
from .forms import *
from .filters import (
    ProductofarmaciaFilter,
)



@login_required
def comprobante_venta(request):

    c_form = ComprobanteForm()
    formset = ProductoVendidoFormset()
    
    if request.method == 'POST':
        cv = ComprobanteVenta.objects.create(farmaceuta=request.user)
        cv.numero_identificacion = request.POST.get('numero_identificacion')
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
            return redirect('core-home')

    context = {
        'c_form': c_form,
        'formset': formset
    }

    return render(request, 'farmacia/comprobanteventa_form.html', context)

#PRODUCTO FARMACIA
class InicioProductoFarmacia(ListView):
    model = ProductoFarmacia
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductofarmaciaFilter(self.request.GET, queryset=self.get_queryset())
        return context

class DetalleProductoFarmacia(DetailView):
  model = ProductoFarmacia

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