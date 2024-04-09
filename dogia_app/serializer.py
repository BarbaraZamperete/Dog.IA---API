from rest_framework import serializers
from dogia_app.models import Usuario, Raca, Cachorro, Imagem, Combinacao
from datetime import datetime

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"
    
    def create(self, validated_data):
        # Adiciona a data de criação
        validated_data['data_criacao'] = datetime.now()
        # Cria a instância do usuário
        usuario = super().create(validated_data)
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

class CachorroSerializer(serializers.ModelSerializer):
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
    

class CombinacaoSerializer(serializers.ModelSerializer):
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