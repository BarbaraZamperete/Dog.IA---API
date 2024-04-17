from django.shortcuts import render
from django.http import JsonResponse
from .models import Usuario, Raca, Cachorro, Imagem, Combinacao
from .serializer import CustomUserSerializer, UsuarioSerializer, RacaSerializer, CachorroSerializer, ImagemSerializer, CombinacaoSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token



class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

###################################################################################
############################ USUÁRIOS #############################################
@api_view(['GET'])
def usuarios_list(request):
    usuarios = Usuario.objects.select_related('user').all()
    serializer = UsuarioSerializer(usuarios, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def criar_usuario(request):
    # Faça uma cópia mutável dos dados
    mutable_data = request.data.copy()
    
    custom_user_serializer = CustomUserSerializer(data=mutable_data)
    if custom_user_serializer.is_valid():
        custom_user = custom_user_serializer.save()  # Salva o CustomUser
        
        # Adicione o id do CustomUser ao request data para o UsuarioSerializer
        mutable_data['user'] = custom_user.id
        print("***********************************")
        print(custom_user.id)
        usuario_serializer = UsuarioSerializer(data=mutable_data)
        print(usuario_serializer)
        print("----------------------------------------")
        if usuario_serializer.is_valid():
            usuario_serializer.save()
            return Response(usuario_serializer.data, status=status.HTTP_201_CREATED)
        return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(custom_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH'])
def atualizar_usuario(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PATCH":
        custom_user_data = {'email': request.data.get('email')}  # Se necessário, adicione outros campos do CustomUser
        custom_user_serializer = CustomUserSerializer(usuario.user, data=custom_user_data, partial=True)
        if custom_user_serializer.is_valid():
            custom_user = custom_user_serializer.save()  # Atualiza o CustomUser

            usuario_data = request.data.copy()
            usuario_data['user'] = custom_user.id  # Atualiza o id do CustomUser no Usuario
            usuario_serializer = UsuarioSerializer(usuario, data=usuario_data, partial=True)
            if usuario_serializer.is_valid():
                usuario_serializer.save()
                return Response(usuario_serializer.data, status=status.HTTP_200_OK)
            return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(custom_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




###################################################################################
############################ RAÇA #################################################
@api_view(['GET'])
def racas_list(request):
    racas = Raca.objects.all()
    serializer = RacaSerializer(racas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def raca_id(request, pk):
    if request.method == "GET":
        try:
            raca = Raca.objects.get(pk=pk)
        except Raca.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RacaSerializer(raca)
        return Response(serializer.data, status=status.HTTP_200_OK)
    



####################################################################################
############################ CACHORROS #############################################
@api_view(['GET'])
def cachorro_list(request):
    cachorro = Cachorro.objects.all()
    serializer = CachorroSerializer(cachorro, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def cachorro_buscados(request):
    cachorro = Cachorro.objects.filter(tipo=1)
    serializer = CachorroSerializer(cachorro, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def cachorro_avistados(request):
    cachorro = Cachorro.objects.filter(tipo=2)
    serializer = CachorroSerializer(cachorro, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def adicionar_cachorro(request):
    serializer = CachorroSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH'])
def atualizar_cachorro(request, pk):
    if request.method == "GET":
        try:
            cachorro = Cachorro.objects.get(pk=pk)
        except Cachorro.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CachorroSerializer(cachorro)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PATCH":
        try:
            cachorro = Cachorro.objects.get(pk=pk)
        except Cachorro.DoesNotExist:
            return Response({"error": "Cachorro não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CachorroSerializer(cachorro, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




##################################################################################
############################ IMAGEMS #############################################
@api_view(['GET'])
def imagem_list(request):
    imagem = Imagem.objects.all()
    serializer = ImagemSerializer(imagem, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def upload_imagem(request):
    serializer = ImagemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH'])
def atualizar_imagem(request, pk):
    if request.method == "GET":
        try:
            imagem = Imagem.objects.get(pk=pk)
        except Imagem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ImagemSerializer(imagem)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PATCH":
        try:
            imagem = Imagem.objects.get(pk=pk)
        except Imagem.DoesNotExist:
            return Response({"error": "Imagem não encontrada."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ImagemSerializer(imagem, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



##################################################################################
############################ COMBINACAO #############################################

@api_view(['GET'])
def combinacao_list(request):
    combinacao = Combinacao.objects.all()
    serializer = CombinacaoSerializer(combinacao, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def adicionar_combinacao(request):
    id_cachorro = request.data.get('id_cachorro')

    try:
        cachorro = Cachorro.objects.get(pk=id_cachorro)
    except Cachorro.DoesNotExist:
        return Response({"error": "Cachorro não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    # Verifica se o ID pertence a um cachorro buscado
    if cachorro.tipo == 1:
        cachorros_avistados = Cachorro.objects.filter(tipo=2)
        for avistado in cachorros_avistados:
            combinacao = Combinacao.objects.create(
                score=0.0,  # Defina a pontuação inicial conforme necessário
                distancia = 0.0,
                score_bruto=0.0,  # Defina a pontuação inicial conforme necessário
                distancia_bruta = 0.0,
                id_buscado=cachorro,
                id_avistado=avistado
            )
            combinacao.save()
    # Verifica se o ID pertence a um cachorro avistado
    elif cachorro.tipo == 2:
        cachorros_buscados = Cachorro.objects.filter(tipo=1)
        for buscado in cachorros_buscados:
            combinacao = Combinacao.objects.create(
                score=0.0,  # Defina a pontuação inicial conforme necessário
                distancia = 0.0,
                score_bruto=0.0,  # Defina a pontuação inicial conforme necessário
                distancia_bruta = 0.0,
                id_buscado=buscado,
                id_avistado=cachorro
            )
            combinacao.save()
    else:
        return Response({"error": "Tipo de cachorro inválido."}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Combinações criadas com sucesso."}, status=status.HTTP_201_CREATED)