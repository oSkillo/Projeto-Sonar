from django.urls import path
from . import views
from conta import views
from conteudo import views

urlpatterns = [
    # Mapeia o URL para a view 'perfil_usuario' e nomeia o caminho como 'perfil'
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('register/', views.register, name='register'),
    
    # Se você quiser adicionar funcionalidade para mudar a senha (opcional)
    # path('mudar_senha/', views.mudar_senha, name='mudar_senha'), 
    
    # Você pode ter outras URLs aqui (login, logout, etc.)
]