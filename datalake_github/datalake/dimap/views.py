from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
)

from .models import (
    Esterilizacion,
)
from .forms import (
    EsterilizacionModelForm,
)
from .filters import (
    EsterilizacionFilter,
)

class InicioEsterilizacion(ListView):
    model = Esterilizacion
    ordering = ['-created']
    context_object_name = 'post'
    template_name = 'dimap/esterilizacion_inicio.html'

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['filter'] = EsterilizacionFilter(self.request.GET, queryset=self.get_queryset())
        return context

@login_required
def esterilizacion_form(request):
    form = EsterilizacionModelForm()
    if request.method == 'POST':
        form = EsterilizacionModelForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.autor = request.user
            obj.save()
            form_id = obj.id
            messages.success(request, f'El Formulario fue creado con exito')
            return redirect('esterilizacion-detail',pk=form_id)

    context = {
        'form':form
    }

    return render(request, 'dimap/esterilizacion_form.html', context)

@login_required
def esterilizacion_detail(request, pk):
    obj = Esterilizacion.objects.get(pk=pk)

    context = {
        'object':obj
    }

    return render(request, 'dimap/esterilizacion_detalle.html', context)

@login_required
def esterilizacion_delete(request, pk):
    obj = Esterilizacion.objects.get(pk=pk)

    if request.method == 'POST':
        if request.user == obj.autor:
            obj.delete()
            messages.success(request, f'El formulario fue eliminado con exito')
            return redirect('esterilizacion-inicio')
        else:
            messages.warning(request, f'No esta autorizado para eliminar el formulario')
            return redirect('esterilizacion-inicio')

    context = {
        'object': obj,
    }

    return render(request, 'dimap/esterilizacion_delete.html', context)