from django.db import models

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

    def __str__(self):
        return self.nome

class Serie(models.Model):
    nome = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    
    #aqui ta definido quais matérias essa série tem
    materias = models.ManyToManyField(Materia, related_name='series')

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
