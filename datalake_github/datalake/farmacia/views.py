from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, UpdateView

@login_required
def comprobante_venta(request, pk):


    c_form = ComprobanteForm()
    pv_form = ProductoVendidoForm()

    if request.method == 'POST':
        c_form = ComprobanteForm(request.POST)
        pv_form = ProductoVendidoForm(request.POST)
        if c_form.is_valid() and pv_form.is_valid():
            c_form.save()
            pv_form.save()
            messages.success(request, f'El comporbante de venta fue creado con exito')
            return redirect('core-home')

    context = {
        'c_form': c_form,
        'pv_form': pv_form
    }


    return render(request, 'farmacia/comprobanteventa.html', context)


