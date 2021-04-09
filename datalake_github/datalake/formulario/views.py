from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from .models import (
    CallesCondiciones,
    Paises,
    FormularioOMIL,
    Seguridad,
    Farmacia,
)

#FORMULARIO OMIL 

class DetalleFormularioOMIL(DetailView):
  model = FormularioOMIL

class CrearFormularioOMIL(LoginRequiredMixin, CreateView):
    model = FormularioOMIL
    fields = [
            'p_origen',
            'tipo_identificacion',
            'numero_identificacion',
            'direccion',
            'nombre',
            'apellido',
            'numero_calle',
            'texto1',
            'texto2',
            'texto3',
            'texto4',
            ]

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class EdicionFormularioOMIL(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = FormularioOMIL
    fields = [
            'p_origen',
            'tipo_identificacion',
            'numero_identificacion',
            'direccion',
            'nombre',
            'apellido',
            'numero_calle',
            'texto1',
            'texto2',
            'texto3',
            'texto4',
            ]

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        formulario = self.get_object()
        if self.request.user == formulario.autor:
            return True
        return False

#FORMULARIO SEGURIDAD

class DetalleSeguridad(DetailView):
  model = Seguridad

class CrearSeguridad(LoginRequiredMixin, CreateView):
    model = Seguridad
    fields = [
            'nombre',
            'apellido',
            'c_telefono',
            'n_telefono',
            'direccion',
            'numero_calle',
            'complemento_direccion',
            'res_denuncia',
            'tipi_reclamo',
            'tipi_denuncia',
            'cuadrante',
            'n_movil',
            'emergencias',
            'derv_emergencias',
            'des_caso',
            'iden_carab',
            'iden_aav',
            'departamento',
            'inf_general',
            ]

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class EdicionSeguridad(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Seguridad
    fields = [
            'nombre',
            'apellido',
            'c_telefono',
            'n_telefono',
            'direccion',
            'numero_calle',
            'complemento_direccion',
            'res_denuncia',
            'tipi_reclamo',
            'tipi_denuncia',
            'cuadrante',
            'n_movil',
            'emergencias',
            'derv_emergencias',
            'des_caso',
            'iden_carab',
            'iden_aav',
            'departamento',
            'inf_general',
            ]

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        formulario = self.get_object()
        if self.request.user == formulario.autor:
            return True
        return False

#FORMULARIO FARMACIA

class DetalleFarmacia(DetailView):
  model = Farmacia

class CrearFarmacia(LoginRequiredMixin, CreateView):
    model = Farmacia
    fields = [
            'numero_identificacion',
            'tipo_identificacion',
            'nombre',
            'apellido',
            'direccion',
            'numero_calle',
            'n_ficha',
            'complemento_direccion',
            'c_telefono',
            'n_telefono',
            'fecha_nacimiento',
            'sis_salud',
            'estado_civil',
            'numero_hijos',
            'p_origen',
            'email_form',
            'enfermedad',
            'med_uso_per',
            'lugar_atencion',
            'discapacidad',
            'discapacidad_doc',
            'embarazo',
            'embarazo_doc',
            ]

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class EdicionFarmacia(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Farmacia
    fields = [
            'numero_identificacion',
            'tipo_identificacion',
            'nombre',
            'apellido',
            'direccion',
            'numero_calle',
            'n_ficha'
            'complemento_direccion',
            'c_telefono',
            'n_telefono',
            'fecha_nacimiento',
            'sis_salud',
            'estado_civil',
            'numero_hijos',
            'p_origen',
            'email_form',
            'enfermedad',
            'med_uso_per',
            'lugar_atencion',
            'discapacidad',
            'discapacidad_doc',
            'embarazo',
            'embarazo_doc',
            ]

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        formulario = self.get_object()
        if self.request.user == formulario.autor:
            return True
        return False

#AUTOCOMPLETADO

def autocompete_calles(request):
    if 'term' in request.GET:
        qs = CallesCondiciones.objects.filter(calle__contains=request.GET.get('term'))
        calles = list()
        for calle in qs:
            calles.append(calle.calle)
        return JsonResponse(calles, safe=False)

def autocompete_pais(request):  
    if 'term' in request.GET:
        qs = Paises.objects.filter(nombre__contains=request.GET.get('term'))
        paises = list()
        for pais in qs:
            paises.append(pais.nombre)
        return JsonResponse(paises, safe=False)



