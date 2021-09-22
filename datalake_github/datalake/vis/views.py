from django.shortcuts import render

def vis(request):

    

    return render(request,'vis/index.html')

def inicio_vis(request):
    return render(request,'vis/inicio_vis.html')
