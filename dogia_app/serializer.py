from rest_framework import serializers
from dogia_app.models import CustomUser, Usuario, Raca, Cachorro, Imagem, Combinacao
from datetime import datetime

# Serializador para CustomUser (autenticação)
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']  # Campos necessários para autenticação

        # Configurações adicionais para o campo de senha
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"
    
    def create(self, validated_data):

        password = validated_data.pop('password', None)
        # custom_user = CustomUser.objects.create_user(email=validated_data['email'], password=password)
        id = validated_data['user'].id
        custom_user = CustomUser.objects.get(id = id)
        # Associe o CustomUser recém-criado ao Usuario
        validated_data['user'] = custom_user
        # Adiciona a data de criação
        validated_data['data_criacao'] = datetime.now()
        # Cria a instância do usuário
        usuario = Usuario.objects.create(**validated_data)
        # Retorna a instância criada
        return usuario

    def update(self, instance, validated_data):
        # Adiciona a data de modificação
        validated_data['data_alteracao'] = datetime.now()
        # Atualiza a instância do usuário
        usuario = super().update(instance, validated_data)
        # Retorna a instância atualizada
        return usuario

class RacaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raca
        fields = "__all__"
    def create(self, validated_data):
        # Adiciona a data de criação
        validated_data['data_criacao'] = datetime.now()
        # Cria a instância do cachorro
        raca = super().create(validated_data)
        # Retorna a instância criada
        return raca

    def update(self, instance, validated_data):
        # Adiciona a data de modificação
        validated_data['data_alteracao'] = datetime.now()
        # Atualiza a instância do cachorro
        raca = super().update(instance, validated_data)
        # Retorna a instância atualizada
        return raca

class ImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagem
        fields = '__all__'
    
    def create(self, validated_data):
        # Adiciona a data de criação
        validated_data['data_criacao'] = datetime.now()
        # Cria a instância da imagem
        imagem = super().create(validated_data)
        # Retorna a instância criada
        return imagem

    def update(self, instance, validated_data):
        # Adiciona a data de modificação
        validated_data['data_alteracao'] = datetime.now()
        # Atualiza a instância da imagem
        imagem = super().update(instance, validated_data)
        # Retorna a instância atualizada
        return imagem
    

class CachorroSerializer(serializers.ModelSerializer):
    imagem  = ImagemSerializer(many=True, read_only=True)
    raca_nome = serializers.StringRelatedField(source='raca.nome', read_only=True)
    genero_display = serializers.CharField(source='get_genero_display', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)

    class Meta:
        model = Cachorro
        fields = "__all__"
    
    def create(self, validated_data):
        # Adiciona a data de criação
        validated_data['data_criacao'] = datetime.now()
        # Cria a instância do cachorro
        cachorro = super().create(validated_data)
        # Retorna a instância criada
        return cachorro

    def update(self, instance, validated_data):
        # Adiciona a data de modificação
        validated_data['data_alteracao'] = datetime.now()
        # Atualiza a instância do cachorro
        cachorro = super().update(instance, validated_data)
        # Retorna a instância atualizada
        return cachorro



class CombinacaoSerializer(serializers.ModelSerializer):
    id_buscado = CachorroSerializer()
    id_avistado = CachorroSerializer()
    class Meta:
        model = Combinacao
        fields = '__all__'
    
    def create(self, validated_data):
        # Adiciona a data de criação
        validated_data['data_criacao'] = datetime.now()
        # Cria a instância da imagem
        combinacao = super().create(validated_data)
        # Retorna a instância criada
        return combinacao

    def update(self, instance, validated_data):
        # Adiciona a data de modificação
        validated_data['data_alteracao'] = datetime.now()
        # Atualiza a instância da imagem
        combinacao = super().update(instance, validated_data)
        # Retorna a instância atualizada
        return combinacao