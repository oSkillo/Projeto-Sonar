from django.urls import path, include
from . import views 
from django.contrib import admin
from conta import views
from conteudo import views

urlpatterns = [
    path('', views.home_view, name='base'),
    path('contato/', views.contato_view, name='contato'),
    path('metodologia/', views.metodologia_view, name='metodologia'),
    path('sobre/', views.sobre_view, name='sobre'),
    path('busca/', views.busca_view, name='busca'),
    path('busca-live/', views.buscar_dados_json, name='busca_live'),
    path('materia/<slug:materia_slug>/', views.visualizar_materia, name='visualizar_materia'),
    path('categoria/outras/', views.outras_divergencias, name='outras'),
    path('entrar/', views.login_user, name="entrar" ),
    path('logout_user', views.logout_user, name='sair'),
    path('<slug:divergencia_slug>/', views.detalhe_divergencia, name='divergencias'),
    path('grau/', views.grau_view, name='grau'),
    path('<slug:divergencia_slug>/grau/<slug:grau_slug>/', views.listar_series_com_grau, name='listar_series_com_grau'),
    path('<slug:divergencia_slug>/', views.listar_series_sem_grau, name='listar_series_sem_grau'),
    path('<slug:divergencia_slug>/grau/<slug:grau_slug>/serie/<slug:serie_slug>/', views.listar_materias_com_grau, name='listar_materias_com_grau'),
    path('<slug:divergencia_slug>/grau/<slug:grau_slug>/serie/<slug:serie_slug>/<slug:materia_slug>/pdfs/', views.listar_pdfs_com_grau, name='listar_pdfs_com_grau'),
    path('<slug:divergencia_slug>/serie/<slug:serie_slug>/', views.listar_materias_sem_grau, name='listar_materias_sem_grau'),
    path('<slug:divergencia_slug>/serie/<slug:serie_slug>/<slug:materia_slug>/pdfs/', views.listar_pdfs_sem_grau, name='listar_pdfs_sem_grau'),
    path('admin/', admin.site.urls),
    path('conta/', include('conta.urls')),
    path('conta/', include('django.contrib.auth.urls')),
]