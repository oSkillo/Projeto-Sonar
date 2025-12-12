from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    # Mapeia a URL /perfil/ para a view user_profile
    path('perfil/', views.conta, name='conta'),
    path('perfil/editar/', views.edit_profile, name='edit_profile'),
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('perfil/', include('django.contrib.auth.urls')),
]