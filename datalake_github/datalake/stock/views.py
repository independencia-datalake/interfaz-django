from django.shortcuts import render

# Create your views here.

def stock(request):

    stock = ProductoFarmacia.objects.all()
    mensaje = ''
    for i in stock:
        mensaje =mensaje + str(i)+'\n'
    return render(request,'farmacia/StockTest.html',{'stock':stock} )

class InicioStock(ListView):
    model = BodegaVirtual
    template_name = "farmacia/Stock.html"
    # ordering = ['marca_producto','dosis']

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


    return render(request, 'farmacia/Stock_form.html',{"form":form})

class EdicionStock(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = BodegaVirtual
    form_class = BodegaVirtualForm
    template_name = "farmacia/Stock_update.html"

    # def form_valid(self, form):
    #     form.instance.autor = self.request.user
    #     return super().form_valid(form)

    def test_func(self):
        # formulario = self.get_object()
        # if self.request.user == formulario.autor:
        #     return True
        # return False
        return True

def Stocks(request):
    
    model = BodegaVirtual
    form = BodegaVirtualForm    
    context = {'form':form}
    return render(request,'farmacia/StockTest.html',context)

class createStock(ListView):
    model = BodegaVirtual
    form_class = BodegaVirtualForm
    template_name = "farmacia/Stock_form.html"

    # def form_valid(self, form):
    #     form.instance.autor = self.request.user
    #     return super().form_valid(form)

    def test_func(self):
        # formulario = self.get_object()
        # if self.request.user == formulario.autor:
        #     return True
        # return False
        return True