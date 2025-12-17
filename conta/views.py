from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .forms import RegisterForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Cria sua views

def cadastro(request):
    if request.method=="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Bem vindo {username}, sua conta foi criada com sucesso!')
            return redirect('login')
      
    form = RegisterForm()
    return render(request, "cadastro.html", {'form':form})

def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

@login_required
def perfil(request):
    return render(request, 'perfil.html')