from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home_view, name='base'),
    path('contato/', views.contato_view, name='contato'),
    path('sobre/', views.sobre_view, name='sobre'),
]