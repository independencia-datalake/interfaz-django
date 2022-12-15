from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.contrib import messages
from farmacia.models import ProductoFarmacia
from farmacia.forms import ComprobanteVentaModelForm
from .models import (
    BodegaVirtual,
    OrdenIngresoProducto,
    OrdenIngresoList,
    ProductoIngresado,
    ProductoMermado,
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


#STATUS (IMITACION DE LOS JSON)
INGRESO_STOCK_STATUS = []

# Create your views here.

class InicioStock(ListView):
    template_name = "stock/Stock.html"
    context_object_name = 'filtrados'
    paginate_by = 10
    model = BodegaVirtual

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = Stockfilter(self.request.GET, queryset=self.get_queryset())
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        return Stockfilter(self.request.GET, queryset=queryset).qs
    def get_paginate_by(self, queryset):

        return self.request.GET.get('paginate_by', self.paginate_by)

@login_required
def crear_producto_Stock(request):
    form = BodegaVirtualcrearForm()

    if request.method == 'POST':
        form = BodegaVirtualcrearForm(request.POST)
        if form.is_valid():
            BodegaVirtual(nombre=form.cleaned_data.get('nombre'),
                            stock=form.cleaned_data.get('stock'),
                            stock_min=form.cleaned_data.get('stock_min'),
                            stock_max =form.cleaned_data.get('stock_max')).save()
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

# def ingreso_producto_stock(response):
#     global INGRESO_STOCK_STATUS

    

#     orden_ingreso_actual = OrdenIngresoProducto.objects.latest('id')
#     if orden_ingreso_actual.estado == True:
#         orden_ingreso_actual = OrdenIngresoProducto.objects.create()
#     ls = orden_ingreso_actual.id
#     temp = INGRESO_STOCK_STATUS
    
#     form = BodegaVirtualIngresoProductoForm
#     form2 = ComprobanteVentaModelForm()
#     context = {"ls":ls,"form":form,"temp":temp, "form2":form2}
#     if response.method == "POST":
#         form = BodegaVirtualIngresoProductoForm(response.POST)
#         if response.POST.get("save"):
#             for i in temp:
#                 ProductoIngresado(
#                         nombre = ProductoFarmacia.objects.get(id=i.get('id_nombre')),
#                         cantidad = i.get('cantidad'),
#                         precio_compra = i.get('precio'),
#                         precio_venta = i.get('precio_venta'),
#                         lote = i.get('lote'),
#                         n_factura = i.get('n_factura'),
#                         n_venta = orden_ingreso_actual).save()

#             INGRESO_STOCK_STATUS = []
#             orden_ingreso_actual.estado = True
#             orden_ingreso_actual.farmaceuta = response.user
#             orden_ingreso_actual.save()
#             messages.success(response, f'El producto fue ingresado con exito')
#             return render(response, "stock/Stock_home.html")

#         elif response.POST.get("newItem") and form.is_valid():
#             nombre = form.cleaned_data.get('nombre')
#             id_nombre = nombre.id
#             cantidad = form.cleaned_data.get('cantidad')
#             precio_compra = form.cleaned_data.get('precio_compra')
#             precio_venta = form.cleaned_data.get('precio_venta')
#             n_venta = orden_ingreso_actual
#             lote = form.cleaned_data.get('lote')
#             n_factura = form.cleaned_data.get('n_factura')
#             # id_lab = Laboratorios.objects.get(nombre_laboratorio=laboratorio).id #todo LO DEL LABORATORIO
#             update_json = {'producto': str(nombre),'id_nombre': id_nombre, 'cantidad': cantidad, 'precio': precio_compra,'precio_venta': precio_venta, 'lote':lote, 'n_factura':n_factura}
#             INGRESO_STOCK_STATUS.append(update_json)

#         elif response.POST.get("cancel"):
#             temp = []
#             INGRESO_STOCK_STATUS = []
#             context = {"ls":ls,"form":form,"temp":temp, "form2":form2}

#     temp = INGRESO_STOCK_STATUS
#     context["temp"]=temp
#     return render(response, "stock/Stock_ingreso.html",context)

def ingreso_producto_stock(response):
    INGRESO_STOCK_LIST = []
    qs = OrdenIngresoList.objects.all()
    for i in qs:
        id_aux = 1
        update = {'producto': i.producto, 'cantidad': i.cantidad_ingresada, 'precio': i.precio_compra,'precio_venta': i.precio_venta, 'lote':i.n_lote, 'n_factura':i.n_factura}
        INGRESO_STOCK_LIST.append(update)

    orden_ingreso_actual = OrdenIngresoProducto.objects.latest('id')
    if orden_ingreso_actual.estado == True:
        orden_ingreso_actual = OrdenIngresoProducto.objects.create()
    ls = orden_ingreso_actual.id
    temp = INGRESO_STOCK_LIST
    
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
                        precio_compra = i.get('precio'),
                        precio_venta = i.get('precio_venta'),
                        lote = i.get('lote'),
                        n_factura = i.get('n_factura'),
                        n_venta = orden_ingreso_actual).save()

            INGRESO_STOCK_STATUS = []
            orden_ingreso_actual.estado = True
            orden_ingreso_actual.farmaceuta = response.user
            orden_ingreso_actual.save()
            messages.success(response, f'El producto fue ingresado con exito')
            return render(response, "stock/Stock_home.html")

        elif response.POST.get("newItem") and form.is_valid():
            nombre = form.cleaned_data.get('nombre')
            id_nombre = nombre.id
            cantidad = form.cleaned_data.get('cantidad')
            precio_compra = form.cleaned_data.get('precio_compra')
            precio_venta = form.cleaned_data.get('precio_venta')
            n_venta = orden_ingreso_actual
            lote = form.cleaned_data.get('lote')
            n_factura = form.cleaned_data.get('n_factura')
            # id_lab = Laboratorios.objects.get(nombre_laboratorio=laboratorio).id #todo LO DEL LABORATORIO
            update_json = {'producto': str(nombre),'id_nombre': id_nombre, 'cantidad': cantidad, 'precio': precio_compra,'precio_venta': precio_venta, 'lote':lote, 'n_factura':n_factura}
            OrdenIngresoList(
                producto = nombre,
                cantidad_ingresada = cantidad,
                precio_compra = precio_compra,
                precio_venta = precio_venta,
                n_lote = lote,
                n_factura = n_factura
            ).save()
            update = {'producto': nombre, 'cantidad': cantidad, 'precio': precio_compra,'precio_venta': precio_venta, 'lote':lote, 'n_factura':n_factura}
            temp.append(update)
        elif response.POST.get("cancel"):
            temp = []
            OrdenIngresoList.objects.all().delete()
            context = {"ls":ls,"form":form,"temp":temp, "form2":form2}

    return render(response, "stock/Stock_ingreso.html",context)
