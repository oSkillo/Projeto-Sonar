from django.urls import path, include
from . import views


urlpatterns = [
<<<<<<< HEAD
    # Mapeia a URL /perfil/ para a view user_profile
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('perfil/editar/', views.edit_profile, name='edit_profile'),
    path('admin/', admin.site.urls),
    path('perfil/', include('django.contrib.auth.urls')),
=======
    
    path('perfil_usuario/', views.perfil_usuario, name='perfil_usuario'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login_user, name="entrar" ),
    path('logout_user', views.logout_user, name='sair'),
    

>>>>>>> 8c89f78859168caad7195464ef4596d5eaed9ce4
]