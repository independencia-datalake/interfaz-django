from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from .models import *

#FORMULARIO BASE
def inicioFormularioBase(request):
    form = FormularioBase.objects.all()

    context = {
        'form': form
    }

    return render(request,'formulario/formulariobase_inicio.html', context)

class DetalleFormularioBase(DetailView):
  model = FormularioBase

class CrearFormularioBase(LoginRequiredMixin, CreateView):
    model = FormularioBase
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

class EdicionFormularioBase(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = FormularioBase
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

#DENUNCIA
def inicioDenuncia(request):
    form = Denuncia.objects.all()

    context = {
        'form': form
    }

    return render(request,'formulario/denuncia_inicio.html', context)


class DetalleDenuncia(DetailView):
  model = Denuncia

class CrearDenuncia(LoginRequiredMixin, CreateView):
    model = Denuncia
    fields = [
            'estatus',
            'tipo_identificacion_denunciante',
            'numero_identificacion_denunciante',
            'nombre_denunciante',
            'apellido_p_denunciante',
            'apellido_m_denunciante',
            'telefono_denunciante',
            'direccion',
            'numero_calle',
            'email_denunciante',
            'tipo_denuncia',
            'texto_denuncia',
            'nombre_denunciado',
            'apellido_p_denunciado',
            'apellido_m_denunciado',
            'telefono_denunciado',
            'direccion_denunciado',
            'numero_calle_denunciado',
            'email_denunciado',
            'fecha_visita',
            'lugar_de_transgresion',
            'visita_inspectiva',
            'texto_observacion',
            'categoria_visita',
            'notificacion',
            'numero_noficacion',
            'texto_enviado',
            'ver_respuesta',
            ]

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class EdicionDenuncia(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Denuncia
    fields = [
            'estatus',
            'tipo_identificacion_denunciante',
            'numero_identificacion',
            'nombre_denunciante',
            'apellido_p_denunciante',
            'apellido_m_denunciante',
            'telefono_denunciante',
            'direccion',
            'numero_calle',
            'email_denunciante',
            'tipo_denuncia',
            'texto_denuncia',
            'nombre_denunciado',
            'apellido_p_denunciado',
            'apellido_m_denunciado',
            'telefono_denunciado',
            'direccion_denunciado',
            'numero_calle_denunciado',
            'email_denunciado',
            'fecha_visita',
            'lugar_de_transgresion',
            'visita_inspectiva',
            'texto_observacion',
            'categoria_visita',
            'notificacion',
            'numero_noficacion',
            'texto_enviado',
            'ver_respuesta',
            ]

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        formulario = self.get_object()
        if self.request.user == formulario.autor:
            return True
        return False

#CONTROL DE PLAGA
def inicioControlDePlaga(request):
    form = ControlDePlaga.objects.all()

    context = {
        'form': form
    }

    return render(request,'formulario/controldeplaga_inicio.html', context)

class DetalleControlDePlaga(DetailView):
  model = ControlDePlaga

class CrearControlDePlaga(LoginRequiredMixin, CreateView):
    model = ControlDePlaga
    fields = [
            'estatus',
            'ficha_numero',
            'tipo_identificacion',
            'numero_identificacion',
            'nombre',
            'apellido_p',
            'apellido_m',
            'telefono',
            'direccion',
            'numero_calle',
            'email',
            'tipo_solicitud',
            'fecha_coordinada',
            'jornada',
            'fecha_visita',
            'producto',
            ]

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class EdicionControlDePlaga(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = ControlDePlaga
    fields = [
            'estatus',
            'ficha_numero',
            'tipo_identificacion',
            'numero_identificacion',
            'nombre',
            'apellido_p',
            'apellido_m',
            'telefono',
            'direccion',
            'numero_calle',
            'email',
            'tipo_solicitud',
            'fecha_coordinada',
            'jornada',
            'fecha_visita',
            'producto',
            ]

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        formulario = self.get_object()
        if self.request.user == formulario.autor:
            return True
        return False

#ESTERILIZACION
def inicioEsterilizacion(request):
    form = Esterilizacion.objects.all()

    context = {
        'form': form
    }

    return render(request,'formulario/esterilizacion_inicio.html', context)

class DetalleEsterilizacion(DetailView):
  model = Esterilizacion

class CrearEsterilizacion(LoginRequiredMixin, CreateView):
    model = Esterilizacion
    fields = [
            'estatus',
            'tipo_identificacion',
            'numero_identificacion',
            'nombre',
            'apellido_p',
            'apellido_m',
            'telefono',
            'direccion',
            'numero_calle',
            'email',
            'mascota',
            'nombre_mascota',
            'sexo_mascota',
            'fecha_cirugia',
            'clinica',
            'asistencia',
            'rechazo',
            ]

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class EdicionEsterilizacion(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Esterilizacion
    fields = [
            'estatus',
            'tipo_identificacion',
            'numero_identificacion',
            'nombre',
            'apellido_p',
            'apellido_m',
            'telefono',
            'direccion',
            'numero_calle',
            'email',
            'mascota',
            'nombre_mascota',
            'sexo_mascota',
            'fecha_cirugia',
            'clinica',
            'asistencia',
            'rechazo',
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



