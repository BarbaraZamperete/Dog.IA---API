from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("usuarios/", views.usuarios_list, name='usuarios_list'),
    path("usuarios/<int:pk>/", views.atualizar_usuario, name='atualizar_usuario'),
    path("usuarios/adicionar/", views.criar_usuario, name='adicionar_usuario'),
    path("racas/", views.racas_list, name='racas_list'),
    path("racas/<int:pk>/", views.raca_id, name='raca_id'),
    path("cachorros/", views.cachorro_list, name='cachorro_list'),
    path("cachorros/buscados", views.cachorro_buscados, name='cachorros_buscados'),
    path("cachorros/avistados", views.cachorro_avistados, name='cachorros_avistados'),
    path("cachorros/<int:pk>/", views.atualizar_cachorro, name='atualizar_cachorro'),
    path("cachorros/adicionar/", views.adicionar_cachorro, name='adicionar_cachorro'),  
    path("imagens/", views.imagem_list, name='imagens_list'),
    path("imagens/adicionar/", views.upload_imagem, name='adicionar_imagem'),
    path("imagens/<int:pk>/", views.atualizar_imagem, name='atualizar_imagem'),
    path("combinacoes/", views.combinacao_list, name='combinacoes_list'),
    path("combinacoes/adicionar", views.adicionar_combinacao, name='adiconar_combinacao'),
    path('login/', views.CustomAuthToken.as_view()),
]
