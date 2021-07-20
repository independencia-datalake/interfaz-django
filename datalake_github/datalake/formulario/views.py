from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse

from .models import (
    CallesCondiciones,
    Paises,
    FormularioBase,
    Denuncia,
    ControlDePlaga,
    Esterilizacion,
)
from .forms import (
    FormularioBaseForm,
    DenunciaForm,
    ControlDePlagaForm,
    EsterilizacionForm,
)
from .filters import (
    FormularioBaseFilter,
    DenunciaFilter,
    ControlDePlagaFilter,
    EsterilizacionFilter,
)



#FORMULARIO BASE
class InicioFormularioBase(ListView):
    model = FormularioBase
    ordering = ['-created']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = FormularioBaseFilter(self.request.GET, queryset=self.get_queryset())
        return context
    
class DetalleFormularioBase(DetailView):
    model = FormularioBase

class CrearFormularioBase(LoginRequiredMixin, CreateView):
    model = FormularioBase
    form_class = FormularioBaseForm

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class EdicionFormularioBase(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = FormularioBase
    form_class = FormularioBaseForm

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        formulario = self.get_object()
        if self.request.user == formulario.autor:
            return True
        return False

#DENUNCIA
class InicioDenuncia(ListView):
    model = Denuncia
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = DenunciaFilter(self.request.GET, queryset=self.get_queryset())
        return context

class DetalleDenuncia(DetailView):
    model = Denuncia

class CrearDenuncia(LoginRequiredMixin, CreateView):
    model = Denuncia
    form_class = DenunciaForm
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class EdicionDenuncia(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Denuncia
    form_class = DenunciaForm

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        formulario = self.get_object()
        if self.request.user == formulario.autor:
            return True
        return False

#CONTROL DE PLAGA
class InicioControlDePlaga(ListView):
    model = ControlDePlaga

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ControlDePlagaFilter(self.request.GET, queryset=self.get_queryset())
        return context

class DetalleControlDePlaga(DetailView):
    model = ControlDePlaga
    
class CrearControlDePlaga(LoginRequiredMixin, CreateView):
    model = ControlDePlaga
    form_class = ControlDePlagaForm

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class EdicionControlDePlaga(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = ControlDePlaga
    form_class = ControlDePlagaForm

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        formulario = self.get_object()
        if self.request.user == formulario.autor:
            return True
        return False

#ESTERILIZACION
class InicioEsterilizacion(ListView):
    model = Esterilizacion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = EsterilizacionFilter(self.request.GET, queryset=self.get_queryset())
        return context

    
class DetalleEsterilizacion(DetailView):
    model = Esterilizacion

class CrearEsterilizacion(LoginRequiredMixin, CreateView):
    model = Esterilizacion
    form_class = EsterilizacionForm

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

class EdicionEsterilizacion(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Esterilizacion
    form_class = EsterilizacionForm

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        formulario = self.get_object()
        if self.request.user == formulario.autor:
            return True
        return False





