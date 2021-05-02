from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, UpdateView
from django.forms import inlineformset_factory

@login_required
def comprobante_venta(request):

    c_form = ComprobanteForm()
    ProductoVendidoFormset = inlineformset_factory(ComprobanteVenta, ProductoVendido, fields=('nombre', 'cantidad'))
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

