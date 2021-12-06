from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    UpdateView,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin, 
    UserPassesTestMixin,
)
from .models import(
    Requerimiento,
)
from .filters import(
    RequerimientoFilter,
)
from .forms import(
    RequerimientoModelForm,
)

class InicioRequerimineto(ListView):
    model = Requerimiento
    ordering = ['-created']
    context_object_name = 'post'
    template_name = 'seguridad/denuncia_inicio.html'

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['filter'] = RequerimientoFilter(self.request.GET, queryset=self.get_queryset())
        return context

@login_required
def requerimiento_form(request, nr):
    form_req = RequerimientoModelForm()

    if request.method == 'POST':
        form_req = RequerimientoModelForm(request.POST)
        if form_req.is_valid():
            req = form_req.save(commit=False)
            req.n_requerimiento = nr
            print(req.n_requerimiento)
            req.autor = request.user
            req.save()
            print(req.n_requerimiento)
            if req.n_requerimiento == 0:
                req.n_requerimiento = req.id
                req.save()
                print(req.n_requerimiento)
            form_id = req.id
            messages.success(request, f'La denuncia fue creada con exito')
            return redirect('denuncia-detalle',pk=form_id)

    context = {
        'form_req':form_req
    }

    return render(request,'seguridad/denuncia_form.html', context)
    
@login_required
def requermineto_detalle(request,pk):
    req = Requerimiento.objects.get(pk=pk)

    context = {
        'req':req
    }

    return render(request, 'seguridad/denuncia_detalle.html', context)

@login_required
def requermineto_delete(request, pk):
    obj = Requerimiento.objects.get(pk=pk)

    if request.method == 'POST':
        if request.user == obj.autor:
            obj.delete()
            messages.success(request, f'La denuncia fue eliminada con exito')
            return redirect('denuncia-inicio')
        else:
            messages.warning(request, f'No esta autorizado para eliminar el formulario')
            return redirect('denuncia-inicio')

    context = {
        'object': obj,
    }

    return render(request, 'seguridad/denuncia_delete.html', context)

class EdicionDenuncia(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Requerimiento
    form_class = RequerimientoModelForm
    template_name = 'seguridad/denuncia_form.html'

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)

    def test_func(self):
        formulario = self.get_object()
        if self.request.user == formulario.autor:
            return True
        return False