from django.contrib import admin
from .models import Divergencia, Grau, Serie, Materia, MaterialPDF

# Isso faz aparecer as tabelas no painel /admin
admin.site.register(Divergencia)
admin.site.register(Grau)
admin.site.register(Serie)
admin.site.register(Materia)
admin.site.register(MaterialPDF)