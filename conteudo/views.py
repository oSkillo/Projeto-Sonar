from django.shortcuts import render, get_object_or_404, redirect
from .models import Divergencia, Grau, Serie, Materia, MaterialPDF, Perfil
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
from unidecode import unidecode

# View da Home (Alterada)
def home_view(request):
    # Pega só quem tem a caixinha marcada
    divergencias_capa = Divergencia.objects.filter(destaque_home=True)
    return render(request, 'divergencias.html', {'items': divergencias_capa})

def grau_view(request):
    return render(request, 'graus.html')

def busca_view(request):
    query = request.GET.get('q')
    divergencias = []
    pdfs = [] # Aqui vamos mandar apenas os PDFs filtrados
    
    if query:
        # Mesma lógica do Live Search, mas sem limitar quantidade
        todas_divs = Divergencia.objects.all()
        divergencias = [d for d in todas_divs if texto_bate(query, d.nome)]

        todos_pdfs = MaterialPDF.objects.all().select_related('materia')
        pdfs = [
            p for p in todos_pdfs 
            if texto_bate(query, p.titulo) or texto_bate(query, p.materia.nome)
        ]

    return render(request, 'busca.html', {
        'query': query,
        'divergencias': divergencias,
        'pdfs': pdfs
    })

def buscar_dados_json(request):
    query = request.GET.get('q', '')
    data = {
        'divergencias': [],
        'materias': [],
        'pdfs': []
    }
    
    if len(query) > 0:
        # SEÇÃO 1: DIVERGÊNCIAS
        # Trazemos tudo e filtramos no Python para garantir a remoção de acentos
        todas_divs = Divergencia.objects.all()
        # Filtra na lista
        filtrados_div = [item for item in todas_divs if texto_bate(query, item.nome)]
        
        for item in filtrados_div[:3]: # Pega só os 3 primeiros
            data['divergencias'].append({
                'nome': item.nome,
                'url': reverse('divergencias', args=[item.slug])
            })

        # SEÇÃO 2: MATÉRIAS
        todas_mats = Materia.objects.all()
        filtrados_mat = [item for item in todas_mats if texto_bate(query, item.nome)]

        for item in filtrados_mat[:5]:
            qtd = MaterialPDF.objects.filter(materia=item).count()
            data['materias'].append({
                'nome': item.nome,
                'info': f"{qtd} arquivos encontrados",
                'url': reverse('visualizar_materia', args=[item.slug])
            })

        # SEÇÃO 3: PDFs (Busca Híbrida: Título OU Nome da Matéria)
        todos_pdfs = MaterialPDF.objects.all().select_related('materia', 'serie')
        
        # A lógica aqui é: O termo bate no Título DO PDF? OU bate no nome da MATÉRIA?
        filtrados_pdf = [
            p for p in todos_pdfs 
            if texto_bate(query, p.titulo) or texto_bate(query, p.materia.nome)
        ]
        
        for item in filtrados_pdf[:6]:
            data['pdfs'].append({
                'titulo': item.titulo,
                'info': f"{item.materia.nome} • {item.serie.nome}",
                'url_arquivo': item.arquivo_pdf.url, 
            })
            
    return JsonResponse(data)

def texto_bate(busca, texto_banco):
    # Transforma "Matemática" em "matematica" e "Busca" em "busca"
    busca_limpa = unidecode(str(busca)).lower()
    alvo_limpo = unidecode(str(texto_banco)).lower()
    return busca_limpa in alvo_limpo

# 2. PÁGINA DE LISTAGEM DA MATÉRIA
def visualizar_materia(request, materia_slug):
    materia = get_object_or_404(Materia, slug=materia_slug)
    pdfs = MaterialPDF.objects.filter(materia=materia).order_by('serie__nome')
    
    return render(request, 'visualizar_materia.html', {
        'materia': materia,
        'pdfs': pdfs
    })

# 2. PÁGINA DA MATÉRIA (Lista os cards)
def visualizar_materia(request, materia_slug):
    materia = get_object_or_404(Materia, slug=materia_slug)
    # Pega todos os PDFs dessa matéria
    pdfs = MaterialPDF.objects.filter(materia=materia).order_by('serie__nome')
    
    return render(request, 'visualizar_materia.html', {
        'materia': materia,
        'pdfs': pdfs
    })

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password )
        if user is not None:
            login(request, user)
            return redirect('base')
        else:
            messages.success(request, ('Usuário ou Senha incorretos. Tente novamente!'))
            return redirect('entrar')
    else:
        return render(request, 'login.html')
    
#View de Logout do usuario    
def logout_user(request):
    logout(request)
    messages.success(request, (''))
    return redirect('base')

@login_required(login_url='entrar') # Se não tiver logado, manda pro login
def perfil_view(request):
    # O Django é inteligente: como usamos OneToOneField, 
    # podemos acessar o perfil direto pelo usuário (request.user.perfil).
    # Mas, por segurança, usamos o get_or_create para evitar erro se o perfil não existir ainda.
    
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)
    
    return render(request, 'perfil.html', {'perfil': perfil})

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

def metodologia_view(request):
    return render(request, 'metodologia.html')


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
    serie = get_object_or_404(Serie,slug=serie_slug)
    materias = serie.materias.all()
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