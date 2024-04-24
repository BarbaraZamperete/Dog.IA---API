from django.db import models
import os
import uuid

from django.contrib.postgres.fields import ArrayField

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Usuario(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='usuario')
    nome = models.CharField(max_length=50)
    telefone = models.CharField(max_length=15, default="")
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_alteracao = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.user.email


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

    nome = models.CharField(max_length=50, default=None, null=True, blank=True)
    raca = models.ForeignKey(Raca, on_delete=models.CASCADE, null=False, related_name='raca')
    genero = models.SmallIntegerField(choices=GENERO_CHOICES)
    status = models.BooleanField(default=True)
    tipo = models.SmallIntegerField(choices=TIPO_CHOICES, null=False, default=1)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=False, related_name='usuario')
    descricao = models.CharField(max_length=255, default='', blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_alteracao = models.DateTimeField(null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.id} - {self.nome}'

    def get_genero_display(self):
        return dict(self.GENERO_CHOICES).get(self.genero)

    def get_tipo_display(self):
        return dict(self.TIPO_CHOICES).get(self.tipo)

def generate_filename(instance, filename):
    # Obtém a extensão do arquivo original
    ext = filename.split('.')[-1]
    # Gera um nome aleatório usando UUID
    random_value = uuid.uuid4().hex[:8]  # Obtemos os primeiros 8 caracteres do UUID como valor aleatório
    # id_string = str(instance.id).zfill(2)
    # Adiciona o ID da foto e o valor aleatório ao nome do arquivo
    filename = f"{random_value}.{ext}"
    # return os.path.join('uploads/', filename)
    return filename

class Imagem(models.Model):
    caminho = models.ImageField(upload_to=generate_filename, null=False)
    embedding = ArrayField(models.FloatField(), blank=True, null=True)
    cachorro = models.ForeignKey(Cachorro, on_delete=models.CASCADE, null=False, related_name='imagem')
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
    