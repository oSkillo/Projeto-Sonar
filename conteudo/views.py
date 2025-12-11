from django.shortcuts import render



def home_view(request):
    return render(request, 'base.html')

def contato_view(request):
    return render(request, 'contato.html')

def sobre_view(request):
    return render(request, 'sobre.html')