from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserChangeForm

# O decorator @login_required garante que apenas usuários logados acessem esta view.

def login_user(request):
    return render(request, "authenticate/login.html", {})

@login_required
def user_profile(request):
    """
    Exibe a página de perfil do usuário logado.
    O objeto 'request.user' já contém todas as informações do usuário atual.
    """
    
    # Podemos passar o objeto user diretamente para o template
    context = {
        'user': request.user
    }
    
    return render(request, 'conta/profile.html', context)

# Se você estivesse usando Class-Based Views:
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views import View
# class UserProfileView(LoginRequiredMixin, View):
#    ...

@login_required
def edit_profile(request):
    """
    View para exibir e processar a edição de perfil do usuário.
    """
    
    # Se a requisição for POST, o formulário foi submetido.
    if request.method == 'POST':
        # Instancia o formulário com os dados POST e a instância atual do usuário
        form = CustomUserChangeForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save() # Salva as alterações no modelo User
            
            # Mensagem de sucesso para o usuário
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            
            # Redireciona de volta para a página de perfil após o sucesso
            return redirect('user_profile')
            
    # Se a requisição for GET (ou o formulário for inválido no POST), exibe o formulário.
    else:
        # Instancia o formulário pré-preenchido com os dados atuais do usuário
        form = CustomUserChangeForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'conta/edit_profile.html', context)