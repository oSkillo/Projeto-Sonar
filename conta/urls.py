from django.urls import path, include
from . import views

urlpatterns = [
    # Mapeia a URL /perfil/ para a view user_profile
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('perfil/editar/', views.edit_profile, name='edit_profile'),
    path('admin/', admin.site.urls),
    path('perfil/', include('django.contrib.auth.urls')),
]