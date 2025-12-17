from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserChangeForm

@login_required 
def perfil_usuario(request):
    """
    Exibe e processa o formulário de edição de perfil.
    A função só pode ser acessada por usuários logados (graças ao @login_required).
    """
    if request.method == 'POST':
        # Instancia o formulário com os dados do POST e a instância do usuário atual
        form = CustomUserChangeForm(request.POST, instance=request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            # Redireciona para a mesma página para evitar reenvio de formulário
            return redirect('perfil') 
        else:
            messages.error(request, 'Erro ao atualizar o perfil. Verifique os campos.')
    else:
        # Para requisições GET, preenche o formulário com os dados do usuário logado
        form = CustomUserChangeForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'conta/perfil_usuario.html', context)

from django.shortcuts import render

# ... suas outras views ...

def edit_profile(request):
    # Lógica temporária apenas para o servidor rodar
    return render(request, 'conta/edit_profile.html')