from django.shortcuts import render
from django.http import JsonResponse
from .models import Usuario, Raca, Cachorro, Imagem, Combinacao
from .serializer import UsuarioSerializer, RacaSerializer, CachorroSerializer, ImagemSerializer, CombinacaoSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, action, permission_classes, authentication_classes
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication
from rest_framework import viewsets


###################################################################################
############################ USUÁRIOS #############################################
class UserViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def get_permissions(self):
        if self.action == 'create':  # Remover permissões para a função create
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Gerar token de autenticação para o usuário recém-criado
        user = serializer.instance  # Instância do usuário recém-criado
        token, created = Token.objects.get_or_create(user=user)

        # Preparar dados de resposta
        response_data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token.key  # Chave do token de autenticação
        }

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'], permission_classes=[AllowAny], authentication_classes=[])
    def usuarios_list(self, request):
        usuarios = self.get_queryset()
        serializer = self.get_serializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def retornar_usuario(self, request, pk=None):
        try:
            usuario = self.get_object()
        except Usuario.DoesNotExist:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserLogIn(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        usuario = Usuario.objects.get(username=username)
        token = Token.objects.get(user=usuario)
        return Response({
            'token': token.key,
            'id': usuario.pk,
            'username': usuario.username
        })



###################################################################################
############################ RAÇA #################################################
@api_view(['GET'])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def cachorro_list(request):
    cachorro = Cachorro.objects.all()
    serializer = CachorroSerializer(cachorro, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def cachorro_get(request, pk):
    try:
        cachorro = Cachorro.objects.get(pk=pk)
    except Cachorro.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CachorroSerializer(cachorro)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def cachorro_buscados(request):
    usuario = request.query_params.get('usuario')
    if usuario:
        if request.user.is_authenticated:
            cachorro = Cachorro.objects.filter(tipo=1, usuario_id=usuario)
        else:
            return Response({"error": "Acesso não autorizado."}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        cachorro = Cachorro.objects.filter(tipo=1)
    serializer = CachorroSerializer(cachorro, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def cachorro_avistados(request):
    usuario = request.query_params.get('usuario')
    if usuario:
        if request.user.is_authenticated:
            cachorro = Cachorro.objects.filter(tipo=2, usuario_id=usuario)
        else:
            return Response({"error": "Acesso não autorizado."}, status=status.HTTP_401_UNAUTHORIZED)
    else:
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

@api_view(['PATCH'])
def atualizar_cachorro(request, pk):
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
@permission_classes([AllowAny])
def combinacao_list(request):
    combinacao = Combinacao.objects.all()
    serializer = CombinacaoSerializer(combinacao, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def combinacoes_por_id_buscado(request, id_buscado):
    combinacoes = Combinacao.objects.filter(id_buscado=id_buscado).order_by('-score')[:10]
    serializer = CombinacaoSerializer(combinacoes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def combinacoes_por_id_avistado(request, id_avistado):
    combinacoes = Combinacao.objects.filter(id_avistado=id_avistado).order_by('-score')[:10]
    serializer = CombinacaoSerializer(combinacoes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
