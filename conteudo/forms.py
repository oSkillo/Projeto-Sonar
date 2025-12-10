from django import forms

class ContatoForm(forms.Form):
    ASSUNTOS = (
        ('acesso', 'Problema de Acesso/Login'),
        ('pagamento', 'Suporte Financeiro / PG'),
        ('conteudo', 'Dúvida sobre Material'),
        ('outro', 'Outros Assuntos'),
    )
    
    nome = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Seu nome completo'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'seu@email.com'}))
    assunto = forms.ChoiceField(choices=ASSUNTOS, widget=forms.Select(attrs={'class': 'form-select'}))
    mensagem = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Descreva seu problema aqui...'}))