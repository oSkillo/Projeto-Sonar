# urls.py do seu projeto principal (ex: meu_projeto/urls.py)

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView # Para a página inicial simples

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 🌟 Inclui as views de autenticação prontas do Django
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Adicionando uma URL de login mais amigável
    path('login/', include('django.contrib.auth.urls')),
    
    # Pagina Inicial (Target de LOGIN_REDIRECT_URL)
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]