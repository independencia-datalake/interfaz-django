from django.contrib.auth import models
from django.db.models import query_utils
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.http import HttpResponse
import pandas as pd
import json
from datetime import datetime
from collections import OrderedDict

from core.models import(
    Persona,
    Telefono,
    Correo,
    Direccion,
    PersonaInfoSalud,
)
from stock.forms import BodegaVirtualForm, BodegaVirtualIngresoStockForm
from stock.models import (
    BodegaVirtual,
    ProductoIngresado
)
from .models import (
    ComprobanteVenta,
    ProductoFarmacia,
    ProductoVendido,
    Laboratorios,
    Recetas,

)
from .forms import (
    ProductoFarmaciaForm,
    ComprobanteVentaModelForm,
    ProductoVendidoForm,
    ProductoVendidoEdicionForm,
    ProductoVendidoInformeForm,
    ProductoVendidoFormset,
    CargaProductoModelForm, #Prueba
    ProductoFarmaciaModelForm,
    PersonaInfoSaludEdicionForm
)
from .filters import (
    ProductoFarmaciaFilter,
    ComprobanteVentaFilter,
    ProductosVendidosFilter,
    PersonaInfoSaludFilter

)

#STATUS (IMITACION DE LOS JSON)
INFORME_VENTAS_STATUS = []
INFORME_VENTA_FECHA_STATUS = dict()
INFORME_VENTA_FECHA_STATUS_ALL = OrderedDict()
cantidad_acumulada = dict()
LAST_FECHA_DATA_ALL = OrderedDict()

# COMPROVANTE VENTA
class InicioComprobanteVenta(ListView):
    model = ComprobanteVenta
    ordering = ['-created']
    context_object_name = 'post'

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['filter'] = ComprobanteVentaFilter(self.request.GET, queryset=self.get_queryset())
        return context

@login_required
def comprobante_venta_form(request, pk):
    persona = Persona.objects.get(pk=pk)
    telefono = Telefono.objects.get(persona=persona)
    correo = Correo.objects.get(persona=persona)
    direccion = Direccion.objects.get(persona=persona)
    info_salud = PersonaInfoSalud.objects.get(persona=persona)

    formset = ProductoVendidoFormset()
    form = ComprobanteVentaModelForm()
    if request.method == 'POST':
        form = ComprobanteVentaModelForm(request.POST, request.FILES)
        files = request.FILES.getlist("file[]")
        formset = ProductoVendidoFormset(request.POST)
        if form.is_valid() and formset.is_valid():

            for form_rev in formset:
                nombre = form_rev.cleaned_data.get('nombre')
                cantidad = form_rev.cleaned_data.get('cantidad')    
                stock_actual = BodegaVirtual.objects.get(nombre=nombre).stock          
                if cantidad > stock_actual:
                    messages.warning(request, f'No hay Stock suficiente del Producto {nombre}, ya que solo quedan {stock_actual} unidades')
                    return redirect('comprobanteventa-create', pk=pk)
            # del nombre, cantidad, stock_actual

            obj = form.save(commit=False)
            obj.comprador = persona
            obj.farmaceuta = request.user
            obj.save()
            cv = obj
            cv_id = obj.id


            for f in files:
                Recetas(receta = f,
                comprobante_venta = cv).save()

            for form in formset:
                nombre = form.cleaned_data.get('nombre')
                cantidad = form.cleaned_data.get('cantidad')
                id_nombre = nombre.id
                precio_venta = ProductoFarmacia.objects.get(id=id_nombre).precio
                if nombre:
                    ProductoVendido(nombre=nombre,
                                    cantidad=cantidad,
                                    precio_venta = precio_venta,
                                    n_venta=cv).save()
            
            return redirect('comprobanteventa-detail',pk=cv_id)

    context = {
        'c_form': form,
        'persona':persona,
        'telefono':telefono,
        'correo':correo,
        'direccion':direccion,
        'info_salud':info_salud,
        'formset':formset,
    }

    return render(request, 'farmacia/comprobanteventa_form.html', context)

@login_required
def comprobante_venta_detail(request, pk):
    c_venta = ComprobanteVenta.objects.get(pk=pk)
    p_vendido = ProductoVendido.objects.filter(n_venta=pk)
    persona = c_venta.comprador
    recetas = Recetas.objects.filter(comprobante_venta=c_venta)
    productos = [producto for producto in p_vendido.values()]
    total = calcular_total(p_vendido, productos)
    st = calcular_subtotales(p_vendido, productos)
    
    holguras = dict()
    msj = "Advertencia \n Los siguientes productos quedaran con bajo Stock despues de la venta\n"
    holgura_flag = False
    for i in p_vendido:
        if BodegaVirtual.objects.get(nombre=i.nombre).holgura <=0:
            holguras[i.nombre]=BodegaVirtual.objects.get(nombre=i.nombre).holgura
            msj = msj + "-"+str(i.nombre) +"\n"
            holgura_flag = True
    holgura_ctx = {
        "msj":msj,
        "flag":holgura_flag,
    }
    holgura_ctx = json.dumps(holgura_ctx)

    context = {
        'c_detail': c_venta,
        'pv_detail': p_vendido,
        'total': total,
        'persona': persona,
        'recetas': recetas,
        'holgura_ctx':holgura_ctx
    }

    return render(request, 'farmacia/comprobanteventa_detail.html', context)

class EdicionComprobanteVenta(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = ProductoVendido 
    form_class = ProductoVendidoEdicionForm
    template_name='farmacia/comprobanteventa_update.html'

    # def form_valid(self, form):
    #     form.instance.autor = self.request.user
    #     return super().form_valid(form)

    def test_func(self):
        # formulario = self.get_object()
        # if self.request.user == formulario.autor:
        #     return True
        # return False
        return True

@login_required
def comprobante_venta_delete(request, pk):
    c_venta = ComprobanteVenta.objects.get(pk=pk)

    if request.method == 'POST':
        if request.user == c_venta.farmaceuta:
            c_venta.delete()
            messages.success(request, f'El comporbante de venta fue eliminado con exito')
            return redirect('farmacia-home')
        else:
            messages.warning(request, f'No esta autorizado para eliminar el comprobante de venta')
            return redirect('comprobanteventa-inicio')

    context = {
        'object': c_venta,
    }

    return render(request, 'farmacia/delete.html', context)

class ProductosVendidosResumen(ListView):
    model = ProductoVendido
    ordering = ['nombre','created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductosVendidosFilter(self.request.GET, queryset=self.get_queryset())
        return context


# PRODUCTO VENDIDO
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
                            precio_venta = ProductoFarmacia.objects.get(id=nombre.id).precio,
                            n_venta=cv).save()

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
        if request.user: #!todo previamente "if request.user == p_vendido.farmaceuta:"
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


# PRODUCTO FARMACIA
class InicioProductoFarmacia(ListView):
    model = ProductoFarmacia
    context_object_name= 'filtrados'
    ordering = ['marca_producto','dosis']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductoFarmaciaFilter(self.request.GET, queryset=self.get_queryset())
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        return ProductoFarmaciaFilter(self.request.GET, queryset=queryset).qs
    def get_paginate_by(self, queryset):

        return self.request.GET.get('paginate_by', self.paginate_by)

@login_required
def crear_producto_farmacia(request):
    form = ProductoFarmaciaForm()
    form2 = BodegaVirtualIngresoStockForm()
    
    if request.method == 'POST':
        laboratorio = request.POST.get('laboratorio')
        try:
            laboratorio = Laboratorios.objects.get(nombre_laboratorio=laboratorio)
            print(laboratorio)
            print('ya existe')
        except:
            laboratorio = Laboratorios.objects.create(nombre_laboratorio=laboratorio)
            print(laboratorio)
            print('ya existe')

        updated_request = request.POST.copy()
        updated_request['laboratorio'] = laboratorio
        print(updated_request)
        form = ProductoFarmaciaModelForm(updated_request)
        form2 = BodegaVirtualIngresoStockForm(request.POST)
        print(form)
        if form.is_valid() and form2.is_valid():
            producto_farmacia = ProductoFarmacia.objects.create(
                autor=request.user,
                marca_producto=form.cleaned_data.get('marca_producto'),
                p_a=form.cleaned_data.get('p_a'),
                dosis=form.cleaned_data.get('dosis'),
                presentacion =form.cleaned_data.get('presentacion'),
                proveedor = form.cleaned_data.get('proveedor'),
                cenabast = form.cleaned_data.get('cenabast'),
                bioequivalencia = form.cleaned_data.get('bioequivalencia'),
                laboratorio = form.cleaned_data.get('laboratorio'),
                )
            stock = 0
            key = ProductoFarmacia.objects.get(id=producto_farmacia.id)
            if form2.cleaned_data.get('stock_min'):
                stock_min = form2.cleaned_data.get('stock_min')
            else:
                stock_min = 0
            BodegaVirtual.objects.create(  nombre = key,
                            stock = stock,
                            stock_min = stock_min)
            
            messages.success(request, f'El producto fue creado con exito')
            return redirect('productofarmacia-create')


    return render(request, 'farmacia/productofarmacia_form.html',{"form":form,"form2":form2} )

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
        return redirect('farmacia-home')

    context = {
        'object': producto_farmacia,
    }

    return render(request, 'farmacia/delete.html', context)



            #FUNCIONALIDADES EXTRAS


# FUNCIONALIDADES
@login_required
def descargar_comprobantes(request):
    q = '''
    SELECT fc.id AS id, 
        cp.numero_identificacion AS ni,
        cp.nombre_persona AS nombre,
        cp.apellido_paterno AS ap,
        cp.apellido_materno AS am,
        us.username as far, 
        fc.created AS created
    FROM farmacia_comprobanteventa fc
    LEFT JOIN core_persona cp 
        ON fc.comprador_id = cp.id
    LEFT JOIN auth_user us
        ON fc.farmaceuta_id = us.id;
    '''
    comporbante_venta = []
    for c in ComprobanteVenta.objects.raw(q):
        comporbante_venta.append({
            "N venta": c.id,
            "comprador": c.nombre + ' ' + c.ap + ' ' + c.am,
            "N identificacion": c.ni,
            "farmaceuta": c.far,
            "created": str(c.created)
        })
    df = pd.DataFrame(comporbante_venta).astype(str)

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

@login_required
def carga_datos(request):
    c_producto_form = CargaProductoModelForm()

    if request.method == 'POST':
        c_producto_form = CargaProductoModelForm(request.POST,request.FILES)
        if c_producto_form.is_valid():
            c_producto_form.save()
            messages.success(request, f'El archivo fue subido con exito')
            return redirect('productofarmacia-inicio')
        
    context = {
        'datos':c_producto_form
    }

    return render(request, 'farmacia/carga_datos.html', context)    

def informeinicio(request):
    
    return render(request,'farmacia/informe_home.html')

def informe_ventas(request):
    global INFORME_VENTAS_STATUS
    global INFORME_VENTA_FECHA_STATUS
    global INFORME_VENTA_FECHA_STATUS_ALL
    global cantidad_acumulada
    global LAST_FECHA_DATA_ALL

    lista_productos = []
    cantidad_productos = []
    for i in INFORME_VENTAS_STATUS:
        lista_productos.append(i.get('producto'))
        cantidad_productos.append(i.get('cantidad'))


    form = ProductoVendidoInformeForm
    context = {'lista_productos':lista_productos,'cantidad_productos':cantidad_productos,'form':form, 'data_fecha': INFORME_VENTA_FECHA_STATUS, 'data_fecha_all': LAST_FECHA_DATA_ALL, 'cantidad_acumulada': cantidad_acumulada}
    if request.method == 'POST':
        form = ProductoVendidoInformeForm(request.POST)
        if request.POST.get("newItem") and form.is_valid():
            nombre = form.cleaned_data.get('nombre')
            cantidad = cantidad_ventas(nombre)
            producto = nombre.marca_producto
            update_json = {'producto': producto,'cantidad': cantidad}

            lista_productos.append(producto)
            cantidad_productos.append(cantidad)

            # INFORME_VENTA_FECHA_STATUS[producto]= productos_by_cantidad_fecha(nombre)
            INFORME_VENTAS_STATUS.append(update_json)

            INFORME_VENTA_FECHA_STATUS.clear()
            var = productos_by_cantidad_fecha(nombre)
            for i in var:
                if i[0] in INFORME_VENTA_FECHA_STATUS.keys():
                    INFORME_VENTA_FECHA_STATUS[i[0]] = INFORME_VENTA_FECHA_STATUS[i[0]] + i[1]
                else:
                    INFORME_VENTA_FECHA_STATUS[i[0]]=i[1]
            data_fecha_all = dict()
            for i in lista_productos:
                name = ProductoFarmacia.objects.get(marca_producto=i)
                producto_aux = productos_by_cantidad_fecha(name)
                for j in producto_aux:
                    if j[0] in INFORME_VENTA_FECHA_STATUS_ALL.keys():
                        INFORME_VENTA_FECHA_STATUS_ALL[j[0]] = INFORME_VENTA_FECHA_STATUS_ALL[j[0]] + j[1]
                    else:
                        INFORME_VENTA_FECHA_STATUS_ALL[j[0]]=j[1]
                lista_falsa = []

                for k in INFORME_VENTA_FECHA_STATUS_ALL.keys():
                    lista_falsa.append([k,INFORME_VENTA_FECHA_STATUS_ALL[k]])

                dict_aux = INFORME_VENTA_FECHA_STATUS_ALL
                dict_aux = json.dumps(dict_aux)
                dict_aux = lista_falsa
                
                # data_fecha_all.append([i,dict_aux])
                data_fecha_all[i]=dict_aux
                LAST_FECHA_DATA_ALL = data_fecha_all
                dict_aux = OrderedDict()
                data_fecha = INFORME_VENTA_FECHA_STATUS_ALL
                INFORME_VENTA_FECHA_STATUS_ALL = OrderedDict()
            if data_fecha == False: dict()
            var = productos_by_cantidad_fecha_acumulado(nombre)
            cantidad_acumulada = OrderedDict()
            for i in var:
                cantidad_acumulada[i[0]]=i[1]
            

            context = {'lista_productos':lista_productos,'cantidad_productos':cantidad_productos, 'form':form, 'data_fecha':data_fecha,'data_fecha_all':data_fecha_all, 'cantidad_acumulada':cantidad_acumulada}

        elif request.POST.get("clean"):
            lista_productos = []
            cantidad_productos = []
            INFORME_VENTAS_STATUS = []

            INFORME_VENTA_FECHA_STATUS.clear()
            LAST_FECHA_DATA_ALL.clear()

            context = {'lista_productos':lista_productos,'cantidad_productos':cantidad_productos,'form':form, 'data_fecha': INFORME_VENTA_FECHA_STATUS}
    
    return render(request, 'farmacia/informe_ventas.html', context)

def cantidad_ventas(producto):
    cantidad = 0
    vendidos = ProductoVendido.objects.filter(nombre=producto)
    for venta in vendidos:        
        cantidad = cantidad + venta.cantidad
    return cantidad
def productos_by_cantidad_fecha(producto):
    producto = ProductoVendido.objects.filter(nombre=producto).order_by('created')
    data = []
    for i in producto:
        date = i.created.strftime("%Y-%m-%d")
        data_aux = [date, i.cantidad]
        data.append(data_aux)
    return data
def productos_by_cantidad_fecha_acumulado(producto):
    producto = ProductoVendido.objects.filter(nombre=producto).order_by('created')
    data = []
    cantidad_aux = 0 
    for i in producto:
        date = i.created.strftime("%Y-%m-%d")
        cantidad_aux = cantidad_aux + i.cantidad
        data_aux = [date,cantidad_aux]
        data.append(data_aux)
    return data

class PersonaInfoSaludList(ListView):
    model = PersonaInfoSalud
    context_object_name= 'filtrados'
    ordering = ['persona']
    paginate_by = 10
    template_name = 'farmacia/personasalud_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PersonaInfoSaludFilter(self.request.GET, queryset=self.get_queryset())
        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        return PersonaInfoSaludFilter(self.request.GET, queryset=queryset).qs
    def get_paginate_by(self, queryset):

        return self.request.GET.get('paginate_by', self.paginate_by)

class EdicionPersonaInfoSalud(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = PersonaInfoSalud
    form_class = PersonaInfoSaludEdicionForm
    template_name = 'farmacia/personainfosalud_update.html'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        formulario = self.get_object()
        # if self.request.user == formulario.autor:
        #     return True
        # return False
        return True