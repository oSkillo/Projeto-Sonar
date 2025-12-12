from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

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