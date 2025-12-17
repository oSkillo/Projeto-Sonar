from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserChangeForm, PerfilForm
from conteudo.models import Perfil
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout



@login_required
def perfil_usuario(request):
    # Garante que o perfil existe (caso tenha sido criado antes do nosso código automático)
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        # Carrega os dois formulários com os dados enviados
        # user_form: cuida do Nome/Email
        # perfil_form: cuida da Foto (note o request.FILES obrigatório para imagem)
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)
        
        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, 'Seu perfil e foto foram atualizados!')
            return redirect('perfil')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        # Se for apenas abrir a página (GET), carrega os dados atuais
        user_form = CustomUserChangeForm(instance=request.user)
        perfil_form = PerfilForm(instance=perfil)

    context = {
        'user_form': user_form,
        'perfil_form': perfil_form
    }
<<<<<<< HEAD
    return render(request, 'conta/perfil_usuario.html', context)

from django.shortcuts import render

# ... suas outras views ...

def edit_profile(request):
    # Lógica temporária apenas para o servidor rodar
    return render(request, 'conta/edit_profile.html')
=======
    
    # Vamos usar o template que está na pasta CONTA
    return render(request, 'perfil_usuario.html', context)


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

    
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password )
        if user is not None:
            login(request, user)
            return redirect('base')
        else:
            messages.error(request, ('Usuário ou Senha incorretos. Tente novamente!'))
            return redirect('entrar')
    else:
        return render(request, 'login.html')
    
def logout_user(request):
    logout(request)
    return redirect('login')
>>>>>>> 8c89f78859168caad7195464ef4596d5eaed9ce4
