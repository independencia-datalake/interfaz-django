from django.shortcuts import render

def vis(request):
    return render(request,'vis/coropleth-non-sdk.html')
