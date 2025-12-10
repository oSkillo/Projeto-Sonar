# meu_app/forms.py

from django import forms
from django.contrib.auth.models import User

# Importamos UserChangeForm para facilitar, mas o modificamos.
# Se você estiver usando um modelo de Usuário customizado, importe-o.
from django.contrib.auth.forms import UserChangeForm

class CustomUserChangeForm(UserChangeForm):
    # Campos que queremos que o usuário edite.
    # Excluímos 'password', 'last_login', 'date_joined' e 'username' (opcionalmente)
    
    # Tornando o email obrigatório no formulário de edição
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'Nome', 
            'Sobrenome', 
            'email'
        )
        # Se quiser permitir que o usuário mude o username:
        # fields = ('username', 'Nome', 'Sobrenome', 'email')

    # Este construtor remove o campo de senha que o UserChangeForm adiciona por padrão.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove a mensagem de ajuda sobre a senha
        if 'password' in self.fields:
             del self.fields['password']