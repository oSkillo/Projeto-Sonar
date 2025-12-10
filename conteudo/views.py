from django.shortcuts import render, redirect
from .forms import ContatoForm  # Importar o formulário que acabámos de criar

# ... (mantém o código que já tenhas aqui) ...

def suporte(request):
    enviado = False
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            # Futuramente aqui enviaremos o e-mail real
            enviado = True
            form = ContatoForm() # Limpa o formulário
    else:
        form = ContatoForm()

    return render(request, 'suporte.html', {'form': form, 'enviado': enviado})