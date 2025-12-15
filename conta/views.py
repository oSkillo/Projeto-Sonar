from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserChangeForm, PerfilForm
from conteudo.models import Perfil


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
    
    # Vamos usar o template que está na pasta CONTA
    return render(request, 'perfil_usuario.html', context)