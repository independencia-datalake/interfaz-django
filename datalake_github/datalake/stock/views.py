from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.contrib import messages
import json

from farmacia.models import ProductoFarmacia
from farmacia.forms import ComprobanteVentaModelForm
from .models import (
    BodegaVirtual,
    OrdenIngresoProducto,
    ProductoIngresado,
    ProductoMermado,
    Laboratorios,
)
from .forms import (
    BodegaVirtualForm,
    BodegaVirtualcrearForm,
    BodegaVirtualsalidaForm,
    BodegaVirtualIngresoProductoForm,
)
from .filters import (
    Stockfilter,
)
# Create your views here.

class InicioStock(ListView):
    model = BodegaVirtual
    template_name = "stock/Stock.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = Stockfilter(self.request.GET, queryset=self.get_queryset())
        return context

@login_required
def crear_producto_Stock(request):
    form = BodegaVirtualcrearForm()

    if request.method == 'POST':
        form = BodegaVirtualcrearForm(request.POST)
        if form.is_valid():
            BodegaVirtual(nombre=form.cleaned_data.get('nombre'),
                            Stock=form.cleaned_data.get('Stock'),
                            Stock_min=form.cleaned_data.get('Stock_min'),
                            Stock_max =form.cleaned_data.get('Stock_max')).save()
            messages.success(request, f'El producto fue creado con exito')
            return redirect('Stock-inicio')


    return render(request, 'stock/Stock_form.html',{"form":form})

class EdicionStock(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = BodegaVirtual
    form_class = BodegaVirtualForm
    template_name = "stock/Stock_update.html"

    # def form_valid(self, form):
    #     form.instance.autor = self.request.user
    #     return super().form_valid(form)

    def test_func(self):
        # formulario = self.get_object()
        # if self.request.user == formulario.autor:
        #     return True
        # return False
        return True

def HomeStock(request):
    
    return render(request,'stock/Stock_home.html')

def salida_producto_stock(request):
    form = BodegaVirtualsalidaForm()

    if request.method == 'POST':
        form = BodegaVirtualsalidaForm(request.POST)
        if form.is_valid():
            ProductoMermado(nombre=form.cleaned_data.get('nombre'),
                            cantidad=form.cleaned_data.get('cantidad'),
                            motivo=form.cleaned_data.get('motivo'),
                            farmaceuta = request.user).save()

            messages.success(request, f'El producto fue retirado con exito')
            return redirect('productostock-salida')
    else:
        form = BodegaVirtualsalidaForm()
    return render(request, 'stock/Stock_salida.html',{"form":form})

def ingreso_producto_stock(response):
    
    orden_ingreso_actual = OrdenIngresoProducto.objects.latest('id')
    if orden_ingreso_actual.estado == True:
        orden_ingreso_actual = OrdenIngresoProducto.objects.create()
    ls = orden_ingreso_actual.id
    with open("stock/ListaIngreso.json","r") as f:
        temp = json.load(f)
    
    form = BodegaVirtualIngresoProductoForm
    form2 = ComprobanteVentaModelForm()
    context = {"ls":ls,"form":form,"temp":temp, "form2":form2}
    if response.method == "POST":
        form = BodegaVirtualIngresoProductoForm(response.POST)
        if response.POST.get("save"):
            for i in temp:
                ProductoIngresado(
                        nombre = ProductoFarmacia.objects.get(id=i.get('id_nombre')),
                        cantidad = i.get('cantidad'),
                        laboratorio = Laboratorios.objects.get(id=i.get('id_lab')),
                        precio_compra = i.get('precio'),
                        n_venta = orden_ingreso_actual,
                        cenabast = i.get('cenabast'),
                        proveedor = i.get('proveedor')).save()
            temp = []
            with open("stock/ListaIngreso.json","w") as file:
                json.dump(temp,file,indent=4)
            orden_ingreso_actual.estado = True
            orden_ingreso_actual.farmaceuta = response.user
            orden_ingreso_actual.save()
            messages.success(response, f'El producto fue ingresado con exito')
            f.close()
            return render(response, "stock/Stock_home.html")
            # return render(response, "stock/Stock_ingreso.html")


        elif response.POST.get("newItem") and form.is_valid():
            nombre = form.cleaned_data.get('nombre')
            id_nombre = nombre.id
            cantidad = form.cleaned_data.get('cantidad')
            precio_compra = form.cleaned_data.get('precio_compra')
            proveedor = form.cleaned_data.get('proveedor')
            laboratorio = form.cleaned_data.get('laboratorio')
            n_venta = orden_ingreso_actual
            cenabast = form.cleaned_data.get('cenabast')
            id_lab = Laboratorios.objects.get(nombre_laboratorio=laboratorio).id

            # ls.productoingresado_set.create(n_venta = n_venta, nombre = nombre, cantidad = cantidad, precio_compra = precio_compra, proveedor = proveedor, laboratorio = laboratorio)
            update_json = {'producto': str(nombre),'id_nombre': id_nombre, 'cantidad': cantidad, 'precio': precio_compra,'cenabast': cenabast, 'proovedor':proveedor, 'laboratorio':str(laboratorio), 'id_lab':id_lab}
            temp.append(update_json)
            with open("stock/ListaIngreso.json","w") as file:
                json.dump(temp,file,indent=4)

        elif response.POST.get("cancel"):
            temp = []
            with open("stock/ListaIngreso.json","w") as file:
                json.dump(temp,file,indent=4)
            context = {"ls":ls,"form":form,"temp":temp, "form2":form2}


    f.close()
    return render(response, "stock/Stock_ingreso.html",context)

