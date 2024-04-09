from django.db import models
import os
import uuid

from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Usuario(models.Model):
    nome = models.CharField(max_length=50)
    login = models.CharField(max_length=20)
    senha = models.CharField()
    telefone = models.CharField(max_length=15, default="")
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_alteracao = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.login


class Raca(models.Model):
    nome = models.CharField(max_length=50)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_alteracao = models.DateTimeField(null=True, blank=True)
    
    def __str__(self) -> str:
        return self.nome
    
class Cachorro(models.Model):
    GENERO_CHOICES = (
        (1, 'Macho'),
        (2, 'Fêmea'),
    )

    TIPO_CHOICES = (
        (1, 'Buscado'),
        (2, 'Avistado'),
    )

    nome = models.CharField(max_length=50, default=None)
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE, null=False, related_name='raca')
    genero = models.SmallIntegerField(choices=GENERO_CHOICES)
    status = models.BooleanField(default=True)
    tipo = models.SmallIntegerField(choices=TIPO_CHOICES, null=False, default=1)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=False, related_name='usuario')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_alteracao = models.DateTimeField(null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.nome}'

def generate_filename(instance, filename):
    # Obtém a extensão do arquivo original
    ext = filename.split('.')[-1]
    # Gera um nome aleatório usando UUID
    random_value = uuid.uuid4().hex[:8]  # Obtemos os primeiros 8 caracteres do UUID como valor aleatório
    # id_string = str(instance.id).zfill(2)
    # Adiciona o ID da foto e o valor aleatório ao nome do arquivo
    filename = f"{random_value}.{ext}"
    return os.path.join('uploads/', filename)

class Imagem(models.Model):
    caminho = models.ImageField(upload_to=generate_filename, null=False)
    embedding = ArrayField(models.FloatField(), blank=True, null=True)
    cachorro = models.ForeignKey(Cachorro, on_delete=models.CASCADE, null=False, related_name='cachorro')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_alteracao = models.DateTimeField(null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.cachorro.id} - {self.caminho.name}"
    

class Combinacao(models.Model):
    score = models.FloatField()
    score_bruto = models.FloatField()
    distancia = models.FloatField()
    distancia_bruta = models.FloatField()
    id_buscado = models.ForeignKey(Cachorro, on_delete=models.CASCADE, null=False, related_name='buscado')
    id_avistado = models.ForeignKey(Cachorro, on_delete=models.CASCADE, null=False, related_name='avistado')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_alteracao = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.id_buscado} - {self.id_avistado}: {self.score}"
    