from django.urls import path
from . import views


urlpatterns = [
    
    path('perfil_usuario/', views.perfil_usuario, name='perfil_usuario'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login_user, name="entrar" ),
    path('logout_user', views.logout_user, name='sair'),
    

]