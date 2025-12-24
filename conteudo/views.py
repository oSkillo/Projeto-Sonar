from django.shortcuts import render, get_object_or_404, redirect
from .models import Divergencia, Grau, Serie, Materia, MaterialPDF, Perfil
from .forms import DivergenciaForm, GrauForm, SerieForm, MateriaForm, MaterialPDFForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q
from unidecode import unidecode
from django.contrib.auth.decorators import user_passes_test


@login_required
def home_view(request):    
    return render(request, 'home.html')

@login_required
def base_view(request):
    # Pega só quem tem a caixinha marcadasS
    divergencias_capa = Divergencia.objects.filter(destaque_home=True)
    return render(request, 'divergencias.html', {'items': divergencias_capa})

def check_admin(user):
    # Permite se for Superuser OU se for do grupo 'Administrador'
    return user.is_superuser or user.groups.filter(name='Administrador').exists()


@login_required
def grau_view(request):
    return render(request, 'graus.html')

@login_required
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

@login_required
def buscar_dados_json(request):
    query = request.GET.get('q', '')
    data = {
        'divergencias': [],
        'materias': [],
        'pdfs': []
    }
    
    if len(query) > 0:
        todas_divs = Divergencia.objects.all()
        filtrados_div = [item for item in todas_divs if texto_bate(query, item.nome)]
        
        nomes_div_vistos = set()
        for item in filtrados_div:
            if item.nome not in nomes_div_vistos:
                data['divergencias'].append({
                    'nome': item.nome,
                    'url': reverse('divergencias', args=[item.slug])
                })
                nomes_div_vistos.add(item.nome)
                if len(data['divergencias']) >= 3: break 

        todas_mats = Materia.objects.all()
        filtrados_mat = [item for item in todas_mats if texto_bate(query, item.nome)]

        nomes_mat_vistos = set()
        
        for item in filtrados_mat:
            if item.nome not in nomes_mat_vistos:
                qtd = MaterialPDF.objects.filter(materia__slug=item.slug).count()
                
                data['materias'].append({
                    'nome': item.nome,
                    'info': f"{qtd} arquivos encontrados",
                    'url': reverse('visualizar_materia', args=[item.slug])
                })
                nomes_mat_vistos.add(item.nome) 
            
            if len(data['materias']) >= 5: break

        todos_pdfs = MaterialPDF.objects.all().select_related('materia', 'serie')
        
        filtrados_pdf = [
            p for p in todos_pdfs 
            if texto_bate(query, p.titulo) or texto_bate(query, p.materia.nome)
        ]
        
        titulos_pdf_vistos = set() 
        
        for item in filtrados_pdf:
            if item.titulo not in titulos_pdf_vistos:
                data['pdfs'].append({
                    'titulo': item.titulo,
                    'info': f"{item.materia.nome} • {item.serie.nome}",
                    'url_arquivo': item.arquivo_pdf.url, 
                })
                titulos_pdf_vistos.add(item.titulo)
            
            if len(data['pdfs']) >= 6: break 
            
    return JsonResponse(data)


def texto_bate(busca, texto_banco):
    # Transforma "Matemática" em "matematica" e "Busca" em "busca"
    busca_limpa = unidecode(str(busca)).lower()
    alvo_limpo = unidecode(str(texto_banco)).lower()
    return busca_limpa in alvo_limpo

@login_required
def visualizar_materia(request, materia_slug):
    materias_encontradas = Materia.objects.filter(slug=materia_slug)
    if not materias_encontradas.exists():
        from django.http import Http404
        raise Http404("Matéria não encontrada")
    materia_principal = materias_encontradas.first()
    pdfs = MaterialPDF.objects.filter(materia__in=materias_encontradas).order_by('serie__nome')
    form_pdf = MaterialPDFForm() 
    return render(request, 'visualizar_materia.html', {
        'materia': materia_principal,
        'pdfs': pdfs,
        'form_pdf': form_pdf
    })

@login_required(login_url='entrar')
def perfil_usuario(request):
    perfil = request.user.perfil 

    if request.method == 'POST':
        # DEBUG: Isso vai mostrar no seu terminal preto o que o formulário enviou
        print("DADOS RECEBIDOS:", request.POST) 

        # Atualiza dados (com os inputs manuais que colocamos no HTML, isso agora vai funcionar)
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()

        # Lógica da Foto
        if request.POST.get('remover_foto') == 'true':
            print("--- REMOVENDO FOTO... ---")
            perfil.foto = None 
            perfil.save()
            messages.success(request, "Foto de perfil removida com sucesso!")
            return redirect('perfil_usuario')

        elif 'foto' in request.FILES:
            perfil.foto = request.FILES['foto']
        
        perfil.save()
        return redirect('perfil_usuario')

    return render(request, 'perfil_usuario.html', {'perfil': perfil})

@login_required
def outras_divergencias(request):
    # Pega só quem NÃO tem a caixinha marcada
    divergencias_outras = Divergencia.objects.filter(destaque_home=False)
    return render(request, 'outras.html', {
        'items': divergencias_outras,
        'titulo': 'Outras Divergências e Síndromes'
    })

@login_required
def contato_view(request):
    return render(request, 'contato.html')

@login_required
def sobre_view(request):
    return render(request, 'sobre.html')

@login_required
def metodologia_view(request):
    return render(request, 'metodologia.html')

@login_required
def detalhe_divergencia(request, divergencia_slug):
    divergencia = get_object_or_404(Divergencia, slug=divergencia_slug)

    if divergencia.tem_graus:
        graus = Grau.objects.filter(divergencia=divergencia)
        return render(request, 'graus.html', {
            'items': graus,
            'divergencia': divergencia
        })
    else:
        series = Serie.objects.filter(divergencia=divergencia)
        
        return render(request, 'series_sem_grau.html', {
            'items': series,
            'divergencia': divergencia
        })


@login_required
def listar_series_com_grau(request, divergencia_slug, grau_slug):
    divergencia = get_object_or_404(Divergencia, slug=divergencia_slug)
    grau = get_object_or_404(Grau, slug=grau_slug, divergencia=divergencia)
    
    # CORREÇÃO AQUI:
    # Filtra por Divergência E Grau
    series = Serie.objects.filter(divergencia=divergencia, grau=grau)
    
    return render(request, 'series_grau.html', {
        'items': series, 
        'divergencia': divergencia,
        'grau': grau,
        'divergencia_slug': divergencia_slug, 
        'grau_slug': grau_slug
    })

@login_required
def listar_series_sem_grau(request, divergencia_slug):
    divergencia = get_object_or_404(Divergencia, slug=divergencia_slug)
    
    # CORREÇÃO AQUI:
    # Antes estava: Serie.objects.all()
    # Agora: Filtra apenas séries desta divergência
    series = Serie.objects.filter(divergencia=divergencia)
    
    return render(request, 'series_sem_grau.html', {
        'items': series, 
        'divergencia': divergencia,
        'divergencia_slug': divergencia_slug
    })

@login_required
def listar_materias_com_grau(request, divergencia_slug, grau_slug, serie_slug):
    divergencia = get_object_or_404(Divergencia, slug=divergencia_slug)
    grau = get_object_or_404(Grau, slug=grau_slug, divergencia=divergencia)
    
    # 1. Busca a Série correta (que pertence a essa divergência/grau)
    serie = get_object_or_404(Serie, slug=serie_slug, divergencia=divergencia, grau=grau)
    
    # 2. Filtra matérias apenas dessa série
    materias = Materia.objects.filter(serie=serie)

    return render(request, 'materias_graus.html', {
        'items': materias, 
        'divergencia': divergencia,
        'grau': grau, 
        'serie': serie,
        'divergencia_slug': divergencia_slug, 
        'grau_slug': grau_slug, 
        'serie_slug': serie_slug
    })

@login_required
def listar_materias_sem_grau(request, divergencia_slug, serie_slug):
    divergencia = get_object_or_404(Divergencia, slug=divergencia_slug)
    
    # Busca a série específica desta divergência
    serie = get_object_or_404(Serie, slug=serie_slug, divergencia=divergencia)
    
    materias = Materia.objects.filter(serie=serie)
    
    return render(request, 'materias_sem_grau.html', {
        'items': materias, 
        'divergencia': divergencia,
        'serie': serie,
        'divergencia_slug': divergencia_slug, 
        'serie_slug': serie_slug
    })

@login_required
def listar_pdfs_com_grau(request, divergencia_slug, grau_slug, serie_slug, materia_slug):
    # 1. Recupera a hierarquia completa para garantir que estamos no lugar certo
    divergencia = get_object_or_404(Divergencia, slug=divergencia_slug)
    grau = get_object_or_404(Grau, slug=grau_slug, divergencia=divergencia)
    serie = get_object_or_404(Serie, slug=serie_slug, divergencia=divergencia, grau=grau)
    
    # 2. Busca a matéria específica DESSA série
    materia = get_object_or_404(Materia, slug=materia_slug, serie=serie)
    
    # 3. Filtra os PDFs que pertencem a essa matéria exata
    pdfs = MaterialPDF.objects.filter(materia=materia)
    
    return render(request, 'pdfs.html', {
        'pdfs': pdfs,
        # Enviamos os objetos pais para o template usar (ex: mostrar nome no título)
        'divergencia': divergencia,
        'grau': grau,
        'serie': serie,
        'materia': materia,
        # Slugs para links se precisar
        'divergencia_slug': divergencia_slug,
        'grau_slug': grau_slug,
        'serie_slug': serie_slug,
        'materia_slug': materia_slug
    })

@login_required
def listar_pdfs_sem_grau(request, divergencia_slug, serie_slug, materia_slug):
    divergencia = get_object_or_404(Divergencia, slug=divergencia_slug)
    
    # Busca série da divergência (sem grau)
    serie = get_object_or_404(Serie, slug=serie_slug, divergencia=divergencia)
    
    # Busca matéria dessa série
    materia = get_object_or_404(Materia, slug=materia_slug, serie=serie)
    
    pdfs = MaterialPDF.objects.filter(materia=materia)
    
    return render(request, 'pdfs.html', {
        'pdfs': pdfs,
        'divergencia': divergencia,
        'serie': serie,
        'materia': materia,
        'divergencia_slug': divergencia_slug,
        'serie_slug': serie_slug,
        'materia_slug': materia_slug
    })

@login_required
def pagina_contato(request):
    if request.method == "POST":
        # Aqui é onde pegamos os dados no futuro
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        mensagem = request.POST.get('mensagem')
        
        print(f"Mensagem recebida de {nome}: {mensagem}") # Vai aparecer no teu terminal preto
        
        # Aqui poderíamos enviar o email ou salvar no banco
        # Por enquanto, só recarregamos a página
        return render(request, 'contato.html', {'sucesso': True})

    return render(request, 'contato.html')

@user_passes_test(check_admin)
def criar_divergencia(request):
    if request.method == 'POST':
        form = DivergenciaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # MENSAGEM DE SUCESSO (Verde)
            messages.success(request, 'Divergência criada com sucesso!') 
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            # MENSAGEM DE ERRO (Vermelho)
            # Mostra o primeiro erro encontrado (ex: "Slug já existe")
            errors = form.errors.as_text()
            messages.error(request, f'Erro ao criar: {errors}')
            
    return redirect('/')

@user_passes_test(check_admin)
def criar_grau(request):
    if request.method == 'POST':
        form = GrauForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('/')

@user_passes_test(check_admin)
def criar_serie(request):
    if request.method == 'POST':
        form = SerieForm(request.POST, request.FILES)
        if form.is_valid():
    
            serie = form.save(commit=False)
            grau_id = request.POST.get('grau_id')            
            divergencia_id = request.POST.get('divergencia_id')

            if divergencia_id: serie.divergencia_id = divergencia_id
            if grau_id: serie.grau_id = grau_id 
            
            serie.save()
            messages.success(request, 'Série adicionada com sucesso!')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, f'Erro ao criar Série: {form.errors}')
            
    return redirect('/')

@user_passes_test(check_admin)
def criar_materia(request):
    if request.method == 'POST':
        form = MateriaForm(request.POST, request.FILES)
        if form.is_valid():
            materia = form.save(commit=False)
            
            # Pega o ID da série pai que vem do HTML
            serie_id = request.POST.get('serie_id')
            
            if serie_id:
                materia.serie_id = serie_id
                
            materia.save()
            messages.success(request, 'Matéria criada com sucesso!')
            return redirect(request.META.get('HTTP_REFERER', '/'))
            
    return redirect('/')

@user_passes_test(check_admin)
def criar_pdf(request):
    if request.method == 'POST':
        form = MaterialPDFForm(request.POST, request.FILES)
        
        if form.is_valid():
            pdf = form.save(commit=False)
            
            divergencia_id = request.POST.get('divergencia_id')
            grau_id = request.POST.get('grau_id')
            serie_id = request.POST.get('serie_id')
            materia_id = request.POST.get('materia_id') 

            if divergencia_id: pdf.divergencia_id = divergencia_id
            if grau_id: pdf.grau_id = grau_id
            if serie_id: pdf.serie_id = serie_id
            if materia_id: pdf.materia_id = materia_id
            
            pdf.save()
            
            messages.success(request, 'PDF adicionado com sucesso!')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            messages.error(request, f'Erro ao enviar PDF: {form.errors}')
            
    return redirect('/')

@user_passes_test(check_admin)
def editar_divergencia(request, id):
    item = get_object_or_404(Divergencia, id=id)
    
    if request.method == 'POST':
        if 'deletar' in request.POST:
            item.delete()
        
            messages.success(request, 'Item removido com sucesso.')
            return redirect('base')
        
        item.nome = request.POST.get('nome')
        item.slug = request.POST.get('slug')
        
        try:
            item.save()
            messages.success(request, 'Alterações salvas com sucesso!')
        except Exception as e:
            messages.error(request, 'Erro ao salvar: Nome ou Slug já existem.')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        return redirect(request.META.get('HTTP_REFERER', '/'))
            
    return redirect('/')

@user_passes_test(check_admin)
def editar_grau(request, id):
    item = get_object_or_404(Grau, id=id)
    if request.method == 'POST':
        if 'deletar' in request.POST:
            item.delete()
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
        form = GrauForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('/')

@user_passes_test(check_admin)
def editar_serie(request, id):
    item = get_object_or_404(Serie, id=id)
    if request.method == 'POST':
        if 'deletar' in request.POST:
            item.delete()
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
        form = SerieForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('/')

@user_passes_test(check_admin)
def editar_materia(request, id):
    item = get_object_or_404(Materia, id=id)
    if request.method == 'POST':
        if 'deletar' in request.POST:
            item.delete()
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
        form = MateriaForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('/')

@user_passes_test(check_admin)
def editar_pdf(request, id):
    item = get_object_or_404(MaterialPDF, id=id)
    if request.method == 'POST':
        if 'deletar' in request.POST:
            item.delete()
            return redirect(request.META.get('HTTP_REFERER', '/'))
        
        form = MaterialPDFForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('/')
