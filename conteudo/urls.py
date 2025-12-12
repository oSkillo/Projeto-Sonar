from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home_view, name='base'),
    path('contato/', views.contato_view, name='contato'),
    path('sobre/', views.sobre_view, name='sobre'),
    path('categoria/outras/', views.outras_divergencias, name='outras'),
    path('<slug:divergencia_slug>/', views.detalhe_divergencia, name='divergencias'),
    path('<slug:divergencia_slug>/grau/<slug:grau_slug>/', views.listar_series_com_grau, name='listar_series_com_grau'),
    path('<slug:divergencia_slug>/grau/<slug:grau_slug>/serie/<slug:serie_slug>/', views.listar_materias_com_grau, name='listar_materias_com_grau'),
    path('<slug:divergencia_slug>/grau/<slug:grau_slug>/serie/<slug:serie_slug>/<slug:materia_slug>/pdfs/', views.listar_pdfs_com_grau, name='listar_pdfs_com_grau'),
    path('<slug:divergencia_slug>/serie/<slug:serie_slug>/', views.listar_materias_sem_grau, name='listar_materias_sem_grau'),
    path('<slug:divergencia_slug>/serie/<slug:serie_slug>/<slug:materia_slug>/pdfs/', views.listar_pdfs_sem_grau, name='listar_pdfs_sem_grau'),
]