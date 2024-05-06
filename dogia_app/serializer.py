from rest_framework import serializers
from dogia_app.models import Usuario, Raca, Cachorro, Imagem, Combinacao, UsuarioAvista
from datetime import datetime
from django.utils import timezone

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Define o campo da senha como write_only

    class Meta:
        model = Usuario
        fields = ('id', 'username', 'telefone', 'password')  # Inclui o campo da senha nos campos serializados
    

    def update(self, instance, validated_data):
        # Adiciona a data de modificação
        validated_data['data_alteracao'] = timezone.now()
        # Atualiza a instância do usuário
        usuario = super().update(instance, validated_data)
        # Retorna a instância atualizada
        return usuario

class UsuarioAvistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsuarioAvista
        fields = ['id', 'telefone', 'data_alteracao']

    def create(self, validated_data):
        validated_data['data_criacao'] = timezone.now()
        usuario_avista = super().create(validated_data)
        return usuario_avista

    def update(self, instance, validated_data):
        instance.telefone = validated_data.get('telefone', instance.telefone)
        instance.data_alteracao = validated_data.get('data_alteracao', instance.data_alteracao)
        instance.save()
        return instance

class RacaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raca
        fields = "__all__"
    def create(self, validated_data):
        # Adiciona a data de criação
        validated_data['data_criacao'] = timezone.now()
        # Cria a instância do cachorro
        raca = super().create(validated_data)
        # Retorna a instância criada
        return raca

    def update(self, instance, validated_data):
        # Adiciona a data de modificação
        validated_data['data_alteracao'] = timezone.now()
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
        validated_data['data_criacao'] = timezone.now()
        # Cria a instância da imagem
        imagem = super().create(validated_data)
        # Retorna a instância criada
        return imagem

    def update(self, instance, validated_data):
        # Adiciona a data de modificação
        validated_data['data_alteracao'] = timezone.now()
        # Atualiza a instância da imagem
        imagem = super().update(instance, validated_data)
        # Retorna a instância atualizada
        return imagem
    

class CachorroSerializer(serializers.ModelSerializer):
    imagem  = ImagemSerializer(many=True, read_only=True)
    raca_nome = serializers.StringRelatedField(source='raca.nome', read_only=True)
    genero_display = serializers.CharField(source='get_genero_display', read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    tutor_telefone = serializers.CharField(source='usuario.telefone', read_only=True)

    class Meta:
        model = Cachorro
        fields = "__all__"
    
    def create(self, validated_data):
        # Adiciona a data de criação
        validated_data['data_criacao'] = timezone.now()
        # Cria a instância do cachorro
        cachorro = super().create(validated_data)
        # Retorna a instância criada
        return cachorro

    def update(self, instance, validated_data):
        # Adiciona a data de modificação
        validated_data['data_alteracao'] = timezone.now()
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
        validated_data['data_criacao'] = timezone.now()
        # Cria a instância da imagem
        combinacao = super().create(validated_data)
        # Retorna a instância criada
        return combinacao

    def update(self, instance, validated_data):
        # Adiciona a data de modificação
        validated_data['data_alteracao'] = timezone.now()
        # Atualiza a instância da imagem
        combinacao = super().update(instance, validated_data)
        # Retorna a instância atualizada
        return combinacao