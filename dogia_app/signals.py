from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.db.models import F, Max, Min, Sum
import os

from .models import Imagem, Combinacao, Cachorro
from .ia.embedding_creation import embedding_creation
from .ia.score_creation import distance_cal, score_creation

@receiver(post_save, sender=Imagem)
def process_image(sender, instance, created, **kwargs):
    if created and not instance.embedding:
        image_path = os.path.join(settings.MEDIA_ROOT, str(instance.caminho))
        embedding_values_np = embedding_creation(image_path)
        embedding_values = embedding_values_np.flatten().tolist()
        instance.embedding = embedding_values
        instance.save()

@receiver(post_save, sender=Combinacao)
def criar_combinacoes(sender, instance, created, **kwargs):
    if created:
        cachorro_buscado = instance.id_buscado
        cachorro_avistado = instance.id_avistado

        img_buscado = Imagem.objects.get(cachorro=cachorro_buscado)
        img_avistado = Imagem.objects.get(cachorro=cachorro_avistado)

        embedding_buscado = img_buscado.embedding
        embedding_avistado = img_avistado.embedding

        distancia_bruta = distance_cal(embedding_buscado, embedding_avistado)
        instance.distancia_bruta = distancia_bruta
        # Obtém o fator de escala usando o Max e Min das distâncias já existentes
        max_distancia = Combinacao.objects.all().aggregate(Max('distancia_bruta'))['distancia_bruta__max'] or 1
        min_distancia = Combinacao.objects.all().aggregate(Min('distancia_bruta'))['distancia_bruta__min'] or 0
        # fator_escala = 1.0 / (max_distancia - min_distancia) if max_distancia != min_distancia else 1.0
        fator_escala = 0.2

        # Normaliza a distância da nova combinação
        distancia = 1 - fator_escala * (distancia_bruta - min_distancia) / (max_distancia - min_distancia)
        instance.distancia = distancia

        # Normaliza o score da nova combinação
        score_bruto = score_creation(cachorro_buscado, cachorro_avistado, distancia)
        instance.score_bruto = score_bruto

        soma_score_bruto = Combinacao.objects.aggregate(soma=Sum('score_bruto'))['soma']
        score_normalizado = score_bruto/soma_score_bruto
        instance.score = score_normalizado

        instance.save()

        # Atualiza as distâncias normalizadas das outras instâncias já salvas
        outras_combinacoes = Combinacao.objects.exclude(pk=instance.pk)
        for outra_combinacao in outras_combinacoes:
            outra_combinacao.distancia = 1 - fator_escala * (outra_combinacao.distancia_bruta - min_distancia) / (max_distancia - min_distancia)
            outra_combinacao.score = outra_combinacao.score_bruto/soma_score_bruto
            outra_combinacao.save()

        