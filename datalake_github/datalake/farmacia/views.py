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

from core.models import(
    Persona,
    Telefono,
    Correo,
    Direccion,
)
from stock.forms import BodegaVirtualForm, BodegaVirtualIngresoStockForm
from stock.models import BodegaVirtual
from .models import (
    ComprobanteVenta,
    ProductoFarmacia,
    ProductoVendido,
    Recetas,
)
from .forms import (
    ProductoFarmaciaForm,
    ComprobanteVentaModelForm,
    ProductoVendidoForm,
    ProductoVendidoInformeForm,
    ProductoVendidoFormset,
    CargaProductoModelForm, #Prueba
)
from .filters import (
    ProductoFarmaciaFilter,
    ComprobanteVentaFilter,
    ProductosVendidosFilter,
)

#STATUS (IMITACION DE LOS JSON)
INFORME_VENTAS_STATUS = []
INFORME_VENTA_FECHA_STATUS = dict()

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

    formset = ProductoVendidoFormset()
    form = ComprobanteVentaModelForm()
    if request.method == 'POST':
        form = ComprobanteVentaModelForm(request.POST, request.FILES)
        files = request.FILES.getlist("file[]")
        formset = ProductoVendidoFormset(request.POST)
        if form.is_valid() and formset.is_valid():
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
        'formset':formset,
    }

    return render(request, 'farmacia/comprobanteventa_form.html', context)

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
    form_class = ComprobanteVentaModelForm
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


# PRODUCTO FARMACIA
class InicioProductoFarmacia(ListView):
    model = ProductoFarmacia
    ordering = ['marca_producto','dosis']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductoFarmaciaFilter(self.request.GET, queryset=self.get_queryset())
        return context


@login_required
def crear_producto_farmacia(request):
    form = ProductoFarmaciaForm()
    form2 = BodegaVirtualIngresoStockForm()
    
    if request.method == 'POST':
        form = ProductoFarmaciaForm(request.POST)
        form2 = BodegaVirtualIngresoStockForm(request.POST)
        if form.is_valid() and form2.is_valid():
            producto_farmacia = ProductoFarmacia.objects.create(autor=request.user,
                            marca_producto=form.cleaned_data.get('marca_producto'),
                            p_a=form.cleaned_data.get('p_a'),
                            dosis=form.cleaned_data.get('dosis'),
                            presentacion =form.cleaned_data.get('presentacion'),
                            precio=form.cleaned_data.get('precio'))
            stck = 0
            key = ProductoFarmacia.objects.get(id=producto_farmacia.id)
            print(key)
            BodegaVirtual.objects.create(  nombre = key,
                            Stock = stck,
                            Stock_min = form2.cleaned_data.get('Stock_min'))
            
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
        return redirect('productofarmacia-inicio')

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

    lista_productos = []
    cantidad_productos = []

    # with open("farmacia/Informe_ventas.json","r") as f:
        # temp = json.load(f)

    for i in INFORME_VENTAS_STATUS:
        lista_productos.append(i.get('producto'))
        cantidad_productos.append(i.get('cantidad'))


    form = ProductoVendidoInformeForm
    context = {'lista_productos':lista_productos,'cantidad_productos':cantidad_productos,'form':form, 'data_fecha': INFORME_VENTA_FECHA_STATUS}
    if request.method == 'POST':
        form = ProductoVendidoInformeForm(request.POST)
        if request.POST.get("newItem") and form.is_valid():
            nombre = form.cleaned_data.get('nombre')
            cantidad = cantidad_ventas(nombre)
            producto = nombre.marca_producto
            update_json = {'producto': producto,'cantidad': cantidad}

            # temp.append(update_json)
            # with open("farmacia/Informe_ventas.json","w") as file:
            #     json.dump(temp,file,indent=4)
            lista_productos.append(producto)
            cantidad_productos.append(cantidad)

            # data_aux = [producto,productos_by_cantidad_fecha(nombre)]
            INFORME_VENTA_FECHA_STATUS[producto]= productos_by_cantidad_fecha(nombre)
            INFORME_VENTAS_STATUS.append(update_json)

            INFORME_VENTA_FECHA_STATUS.clear()
            pez = productos_by_cantidad_fecha(nombre)
            for i in pez:
                INFORME_VENTA_FECHA_STATUS[i[0]]=i[1]

            data_fecha = INFORME_VENTA_FECHA_STATUS
            context = {'lista_productos':lista_productos,'cantidad_productos':cantidad_productos, 'form':form, 'data_fecha':data_fecha}

        elif request.POST.get("clean"):
            lista_productos = []
            cantidad_productos = []
            INFORME_VENTAS_STATUS = []

            INFORME_VENTA_FECHA_STATUS.clear()
            # with open("farmacia/Informe_ventas.json","w") as file:
            #     json.dump(temp,file,indent=4)

            context = {'lista_productos':lista_productos,'cantidad_productos':cantidad_productos,'form':form, 'data_fecha': INFORME_VENTA_FECHA_STATUS}
        

  
    # f.close()
    return render(request, 'farmacia/informe_ventas.html', context)

def cantidad_ventas(producto):
    cantidad = 0
    vendidos = ProductoVendido.objects.filter(nombre=producto)
    for venta in vendidos:        
        cantidad = cantidad + venta.cantidad
    return cantidad
def productos_by_cantidad_fecha(producto):
    cantidad =[]
    fecha = []
    producto = ProductoVendido.objects.filter(nombre=producto) 
    data = []
    for i in producto:
        data_aux = [i.created, i.cantidad]
        data.append(data_aux)
    return data
