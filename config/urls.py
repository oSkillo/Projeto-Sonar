from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from conta import views
from conteudo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('conteudo.urls')),
    path('conta/', include('conta.urls')),
    path('accounts/', include('conta.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)