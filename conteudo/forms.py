from django import forms
from .models import Divergencia, Grau, Serie, Materia, MaterialPDF

class ContatoForm(forms.Form):
    ASSUNTOS = (
        ('acesso', 'Problema de Acesso/Login'),
        ('pagamento', 'Suporte Financeiro / PG'),
        ('conteudo', 'Dúvida sobre Material'),
        ('outro', 'Outros Assuntos'),
    )
    
    nome = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome completo'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Insira sua senha'} ))
    assunto = forms.ChoiceField(choices=ASSUNTOS, widget=forms.Select(attrs={'class': 'form-select'}))
    mensagem = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Descreva seu problema aqui...'}))


class DivergenciaForm(forms.ModelForm):
    class Meta:
        model = Divergencia
        fields = ['nome', 'slug', 'imagem', 'tem_graus', 'destaque_home']
        
        # Vamos adicionar classes CSS para estilizar os inputs
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'input-estilizado', 'placeholder': 'Ex: Sídrome de Down', 'id': 'id_nome_div'}),
            'slug': forms.TextInput(attrs={'class': 'input-estilizado', 'placeholder': 'Ex: down', 'id': 'id_slug_div'}),
            'imagem': forms.FileInput(attrs={'class': 'input-estilizado'}),
            # Checkboxes não precisam da classe input-estilizado padrão, pois são quadrados
            'tem_graus': forms.CheckboxInput(attrs={'class': 'checkbox-custom'}),
            'destaque_home': forms.CheckboxInput(attrs={'class': 'checkbox-custom'}),
        }
        labels = {
            'destaque_home': 'Aparecer na Home?',
            'tem_graus': 'Tem Graus (Níveis de suporte)?'
        }

class GrauForm(forms.ModelForm):
    class Meta:
        model = Grau
        fields = ['divergencia', 'nome', 'slug']
        widgets = {
            'divergencia': forms.Select(attrs={'class': 'input-estilizado'}),
            'nome': forms.TextInput(attrs={'class': 'input-estilizado', 'id': 'id_nome_grau'}),
            'slug': forms.TextInput(attrs={'class': 'input-estilizado', 'id': 'id_slug_grau'}),
        }

class SerieForm(forms.ModelForm):
    class Meta:
        model = Serie
        fields = ['nome', 'slug']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'input-estilizado', 'id': 'id_nome_serie'}),
            'slug': forms.TextInput(attrs={'class': 'input-estilizado', 'id': 'id_slug_serie'}),
        }

class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        # Agora podemos incluir 'series'
        fields = ['nome', 'slug', 'imagem', 'series']
        
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'input-estilizado', 'id': 'id_nome_materia'}),
            'slug': forms.TextInput(attrs={'class': 'input-estilizado', 'id': 'id_slug_materia'}),
            'imagem': forms.FileInput(attrs={'class': 'input-estilizado'}),
            
            # --- WIDGET DAS SÉRIES (Caixinhas de seleção) ---
            'series': forms.CheckboxSelectMultiple(attrs={'class': 'lista-series-checkbox'}),
        }

class MaterialPDFForm(forms.ModelForm):
    class Meta:
        model = MaterialPDF
        fields = ['titulo', 'arquivo_pdf', 'divergencia', 'grau', 'serie', 'materia']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'input-estilizado'}),
            'arquivo_pdf': forms.FileInput(attrs={'class': 'input-estilizado'}),
            'divergencia': forms.Select(attrs={'class': 'input-estilizado'}),
            'grau': forms.Select(attrs={'class': 'input-estilizado'}),
            'serie': forms.Select(attrs={'class': 'input-estilizado'}),
            'materia': forms.Select(attrs={'class': 'input-estilizado'}),
        }