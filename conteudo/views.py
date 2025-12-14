from django.shortcuts import render, get_object_or_404, redirect
from .models import Divergencia, Grau, Serie, Materia, MaterialPDF
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# View da Home (Alterada)
def home_view(request):
    # Pega só quem tem a caixinha marcada
    divergencias_capa = Divergencia.objects.filter(destaque_home=True)
    return render(request, 'divergencias.html', {'items': divergencias_capa})

def grau_view(request):
    return render(request, 'graus.html')

# View de login do usuario
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password )
        if user is not None:
            login(request, user)
            return redirect('base')
        else:
            messages.success(request, ('Houve um erro ao tentar logar, tente novamente!'))
            return redirect('login')
    else:
        return render(request, 'athenticate')
    
#View de Logout do usuario    
def logout_user(request):
    logout(request)
    messages.success(request, ('Você foi deslogado'))
    return redirect('base')

# Nova View para a página "Outras"
def outras_divergencias(request):
    # Pega só quem NÃO tem a caixinha marcada
    divergencias_outras = Divergencia.objects.filter(destaque_home=False)
    return render(request, 'outras.html', {
        'items': divergencias_outras,
        'titulo': 'Outras Divergências e Síndromes'
    })

# ... (Mantenha detalhe_divergencia e as outras views iguais) ...

def contato_view(request):
    return render(request, 'contato.html')

def sobre_view(request):
    return render(request, 'sobre.html')

#aqui é a função q decide o caminho (com grau ou sem grau)

def detalhe_divergencia(request, divergencia_slug):
    divergencia = get_object_or_404(Divergencia, slug=divergencia_slug)

    if divergencia.tem_graus:
        # mostra a lista de graus
        graus = Grau.objects.filter(divergencia=divergencia)
        return render(request, 'graus.html', {
            'items': graus,
            'divergencia': divergencia
        })
    else:
        # pula direto para listar series
        series = Serie.objects.all()
        return render(request, 'series_sem_grau.html', {
            'items': series,
            'divergencia': divergencia
        })

# caminho com grau!!!

def listar_series_com_grau(request, divergencia_slug, grau_slug):
    series = Serie.objects.all()
    return render(request, 'series_grau.html', {
        'items': series, 'divergencia_slug': divergencia_slug, 'grau_slug': grau_slug
    })

def listar_series_sem_grau(request, divergencia_slug):
    series = Serie.objects.all()
    return render(request, 'series_sem_grau.html', {
        'items': series, 'divergencia_slug': divergencia_slug
    })


def listar_materias_com_grau(request, divergencia_slug, grau_slug, serie_slug):
    serie = get_object_or_404(Serie,slug=serie_slug)
    materias = serie.materias.all()
    return render(request, 'materias_graus.html', {
        'items': materias, 'divergencia_slug': divergencia_slug, 'grau_slug': grau_slug, 'serie_slug': serie_slug
    })

def listar_pdfs_com_grau(request, divergencia_slug, grau_slug, serie_slug, materia_slug):
    pdfs = MaterialPDF.objects.filter(
        divergencia__slug=divergencia_slug,
        grau__slug=grau_slug,
        serie__slug=serie_slug,
        materia__slug=materia_slug
    )
    return render(request, 'pdfs.html', {'pdfs': pdfs})


# caminho sem grau!

def listar_materias_sem_grau(request, divergencia_slug, serie_slug):
    materias = Materia.objects.all()
    return render(request, 'materias_sem_grau.html', {
        'items': materias, 'divergencia_slug': divergencia_slug, 'serie_slug': serie_slug
    })

def listar_pdfs_sem_grau(request, divergencia_slug, serie_slug, materia_slug):
    pdfs = MaterialPDF.objects.filter(
        divergencia__slug=divergencia_slug,
        grau__isnull=True,
        serie__slug=serie_slug,
        materia__slug=materia_slug
    )
    return render(request, 'pdfs.html', {'pdfs': pdfs})