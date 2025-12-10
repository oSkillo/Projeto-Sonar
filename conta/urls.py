# meu_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Mapeia a URL /perfil/ para a view user_profile
    path('perfil/', views.conta, name='conta'),
    path('perfil/editar/', views.edit_profile, name='edit_profile'),
]