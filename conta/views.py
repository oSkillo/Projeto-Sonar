from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserChangeForm, PerfilForm
from conteudo.models import Perfil
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout



@login_required
def perfil_usuario(request):
    # Garante que o perfil existe
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        # Carrega os formulários com os dados enviados
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)
        
        if user_form.is_valid() and perfil_form.is_valid():
            # 1. Salva os dados do usuário (Nome, Email, etc)
            user_form.save()

            # 2. LÓGICA DE REMOVER FOTO
            # Verificamos o campo hidden que criamos no HTML
            if request.POST.get('remover_foto') == 'true':
                print("--- REMOVENDO FOTO (App Conta) ---") # Debug no terminal
                perfil.foto = 'perfis/default.png' # Define a imagem padrão
                perfil.save() # Salva diretamente no banco
            else:
                # Se NÃO clicou em remover, deixa o form salvar (caso tenha upload novo)
                perfil_form.save()
            
            messages.success(request, 'Seu perfil e foto foram atualizados!')
            return redirect('perfil_usuario')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        # GET: Carrega os dados atuais
        user_form = CustomUserChangeForm(instance=request.user)
        perfil_form = PerfilForm(instance=perfil)

    context = {
        'user_form': user_form,
        'perfil_form': perfil_form
    }
    
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
            return redirect('home')
        else:
            messages.error(request, ('Usuário ou Senha incorretos. Tente novamente!'))
            return redirect('entrar')
    else:
        return render(request, 'login.html')
    
def logout_user(request):
    logout(request)
    return redirect('login')