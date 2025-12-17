from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name='conta'

urlpatterns = [
    # Mapeia o URL para a view 'perfil_usuario' e nomeia o caminho como 'perfil'
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Se você quiser adicionar funcionalidade para mudar a senha (opcional)
    # path('mudar_senha/', views.mudar_senha, name='mudar_senha'), 
    
    # Você pode ter outras URLs aqui (login, logout, etc.)
]