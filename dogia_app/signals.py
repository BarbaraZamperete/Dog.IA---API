from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.db.models import F, Max, Min, Sum
import os

from .models import Imagem, Combinacao, Cachorro, Raca
from .ia.breed_classification import breed
from .ia.embedding_creation import embedding_creation
from .ia.score_creation import distance_cal, score_creation
from .ia.dog_box import create_box

def calc_min_distancia():
    return Combinacao.objects.all().aggregate(Min('distancia_bruta'))['distancia_bruta__min'] or 0

def calc_max_distancia():
    return Combinacao.objects.all().aggregate(Max('distancia_bruta'))['distancia_bruta__max'] or 1

def calc_distancia(distancia_bruta ):
    max_distancia = calc_max_distancia()
    min_distancia = calc_min_distancia()
    fator_escala = 0.2

    return (1 - fator_escala * (distancia_bruta - min_distancia) / (max_distancia - min_distancia))

def calc_score(score_bruto):
    soma_score_bruto = Combinacao.objects.aggregate(soma=Sum('score_bruto'))['soma']
    if soma_score_bruto != 0:
        score_normalizado = score_bruto/soma_score_bruto
    else:
        score_normalizado = score_bruto
    return score_normalizado

def update_combinacoes(id):
    outras_combinacoes = Combinacao.objects.exclude(pk=id)
    for outra_combinacao in outras_combinacoes:
        outra_combinacao.distancia = calc_distancia(outra_combinacao.distancia_bruta)
        outra_combinacao.score = calc_score(outra_combinacao.score_bruto)
        outra_combinacao.save()

@receiver(post_save, sender=Imagem)
def process_image(sender, instance, created, **kwargs):
    if created and not instance.embedding:
        image_path = os.path.join(settings.MEDIA_ROOT, str(instance.caminho))
        # Geração das bouding boxes
        xml_output_path = os.path.splitext(image_path)[0] + '.xml'
        image_com_box = create_box(image_path, xml_output_path)
        #Geraçao dos embbedings a partir da imagem recortada
        embedding_values_np = embedding_creation(image_com_box)
        embedding_values = embedding_values_np.flatten().tolist()
        instance.embedding = embedding_values
        instance.save()

        racas = Raca.objects.all().order_by('id')
        print(racas)

        # Obter a raça e a pontuação da imagem
        raca_certeza, raca = breed(image_path, racas)
        print(raca)
        print(raca_certeza)

        # Obter a instância do cachorro correspondente
        cachorro = Cachorro.objects.get(id=instance.cachorro.id)

        # Atualizar os campos de raça e pontuação
        cachorro.raca = raca
        cachorro.raca_certeza = float(raca_certeza)

        # Salvar as mudanças
        cachorro.save()

        if (instance.cachorro.tipo == 1):
        
            # Get all images of opposite type
            imgs_cachorros_1 = Imagem.objects.filter(cachorro__tipo=2, cachorro__status=True)

            # Create combinations with the new image and all opposite type images
            for img_1 in imgs_cachorros_1:
                comb = Combinacao.objects.create(
                    score=0.0,  # Defina a pontuação inicial conforme necessário
                    distancia = 0.0,
                    score_bruto=0.0,  # Defina a pontuação inicial conforme necessário
                    distancia_bruta = 0.0,
                    id_buscado=instance.cachorro,
                    id_avistado=img_1.cachorro
                )
                # Calculate and set distance, score, etc. (similar to your existing logic)

                emb_1 = instance.embedding
                emb_2 = img_1.embedding

                distancia_bruta = distance_cal(emb_1, emb_2)
                comb.distancia_bruta = distancia_bruta

                comb.distancia = calc_distancia(distancia_bruta)

                score_bruto = score_creation(instance.cachorro, img_1.cachorro, comb.distancia)
                comb.score_bruto = score_bruto  

                comb.score = calc_score(score_bruto)

                comb.save()

                update_combinacoes(comb.id)

        
        if (instance.cachorro.tipo == 2):
        
            # Get all images of opposite type
            imgs_cachorros_1 = Imagem.objects.filter(cachorro__tipo=1, cachorro__status=True)

            # Create combinations with the new image and all opposite type images
            for img_1 in imgs_cachorros_1:
                comb = Combinacao.objects.create(
                    score=0.0,  # Defina a pontuação inicial conforme necessário
                    distancia = 0.0,
                    score_bruto=0.0,  # Defina a pontuação inicial conforme necessário
                    distancia_bruta = 0.0,
                    id_buscado=img_1.cachorro,
                    id_avistado=instance.cachorro
                )
                # Calculate and set distance, score, etc. (similar to your existing logic)

                emb_2 = instance.embedding
                emb_1 = img_1.embedding

                distancia_bruta = distance_cal(emb_1, emb_2)
                comb.distancia_bruta = distancia_bruta

                comb.distancia = calc_distancia(distancia_bruta)

                score_bruto = score_creation(img_1.cachorro, instance.cachorro, comb.distancia)
                comb.score_bruto = score_bruto  

                comb.score = calc_score(score_bruto)

                comb.save()
                update_combinacoes(comb.id)





@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(pre_delete, sender=Cachorro)
def delete_cachorro_images(sender, instance, **kwargs):
    # Excluir imagens associadas ao cachorro ao excluir o cachorro
    for imagem in instance.imagem.all():
        # Obter o caminho do arquivo XML
        print(imagem.caminho.path)
        image_path = imagem.caminho.path
        xml_path = os.path.splitext(image_path)[0] + '.xml'
        
        # Verificar se o arquivo XML existe e excluí-lo
        if os.path.exists(xml_path):
            os.remove(xml_path)

        imagem.caminho.delete()  # Exclui a imagem do diretório de uploads
        
