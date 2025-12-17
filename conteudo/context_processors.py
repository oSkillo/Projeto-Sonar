from .models import Divergencia

def divergencias_sidebar(request):
    # Busca todas as divergências que tem o 'destaque_home' marcado
    divergencias_destaque = Divergencia.objects.filter(destaque_home=True)
    
    # Retorna para usar no HTML com o nome 'sidebar_divergencias'
    return {
        'sidebar_divergencias': divergencias_destaque
    }