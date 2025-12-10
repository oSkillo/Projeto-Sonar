from django.urls import path
from conteudo import views  # <--- IMPORTANTE: Importar do app 'conteudo'

urlpatterns = [
    # ... outras rotas ...
    path('suporte/', views.suporte, name='suporte'), 
]