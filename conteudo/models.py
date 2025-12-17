from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    # O OneToOneField garante que cada usuário tenha apenas UM perfil
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    
    # Se o usuário não enviar foto, usaremos uma imagem padrão
    foto = models.ImageField(upload_to='perfis/', default='perfis/default.png')

    def __str__(self):
        return f"Perfil de {self.usuario.username}"


class Divergencia(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    imagem = models.ImageField(upload_to='divergencias/', blank=True, null=True)
    tem_graus = models.BooleanField(default=False)
    destaque_home = models.BooleanField(default=False, verbose_name="Aparecer na Home?")

    def __str__(self):
        return self.nome

class Grau(models.Model):
    divergencia = models.ForeignKey(Divergencia, on_delete=models.CASCADE, related_name='graus')
    nome = models.CharField(max_length=50)
    slug = models.SlugField() 

    def __str__(self):
        return f"{self.divergencia.nome} - {self.nome}"

class Materia(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    imagem = models.ImageField(upload_to='materias/', blank=True, null=True)
    
    # O relacionamento fica AQUI agora.
    # O related_name='materias' garante que suas views antigas (serie.materias.all) continuem funcionando!
    series = models.ManyToManyField('Serie', related_name='materias', blank=True) 

    def __str__(self):
        return self.nome

class Serie(models.Model):
    nome = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    

    def __str__(self):
        return self.nome

class MaterialPDF(models.Model):
    titulo = models.CharField(max_length=200)
    divergencia = models.ForeignKey(Divergencia, on_delete=models.CASCADE)
    grau = models.ForeignKey(Grau, on_delete=models.CASCADE, null=True, blank=True)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    arquivo_pdf = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.titulo

@receiver(post_save, sender=User)
def criar_perfil_automatico(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)