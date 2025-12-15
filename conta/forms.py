from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
# Importamos o modelo Perfil que está lá no outro app (conteudo)
from conteudo.models import Perfil

# Obtém o modelo de usuário ativo, seja o padrão ou o customizado.
User = get_user_model() 

class CustomUserChangeForm(UserChangeForm):
    # Opcional: Aqui você pode adicionar campos específicos que não estão no modelo base.
    
    class Meta:
        model = User
        # CAMPOS CORRETOS: use os nomes exatos do seu modelo de usuário
        fields = ('first_name', 'last_name', 'email') 
        # Se você estiver usando um campo 'username' e quiser exibi-lo:
        # fields = ('username', 'first_name', 'last_name', 'email')
        
    # Remove o campo 'password' do formulário. Ele é gerenciado separadamente.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto']

# Obtém o modelo de usuário ativo (padrão ou customizado)
User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    # Aqui você pode adicionar campos extras se precisar, 
    # ou apenas definir o Model/Fields
    class Meta:
        model = User
        fields = ('username', 'email', 'password ') # Exemplo: pedindo username e email
        # O UserCreationForm já trata as senhas por padrão