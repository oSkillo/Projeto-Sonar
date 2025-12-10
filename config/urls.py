# urls.py do seu projeto principal (ex: meu_projeto/urls.py)

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    # ... outras rotas ...
    path('', include('conteudo.urls')), 
]