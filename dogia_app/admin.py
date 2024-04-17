from django.contrib import admin
from .models import Usuario, Raca, Cachorro, Imagem, Combinacao

# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'data_criacao', 'data_alteracao')
    list_display_links = ('id', 'nome')
    search_fields = ('nome',)

class RacaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'data_criacao', 'data_alteracao')
    list_display_links = ('id', 'nome')
    search_fields = ('id', 'nome')

class CachorroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'genero','raca', 'tipo', 'status')
    list_display_links = ('id', 'nome')
    search_fields = ('id', 'nome', 'status')
    list_editable = ('status',)

class ImagemAdmin(admin.ModelAdmin):
    list_display = ('id', 'caminho', 'cachorro')
    list_display_links = ('id', 'caminho')
    search_fields = ('id', 'caminho')

class CombinacaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_buscado', 'id_avistado', 'score', 'distancia')
    list_display_links = ('id', 'id_buscado', 'id_avistado')
    search_fields = ('id', 'id_buscado', 'id_avistado')


admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Raca, RacaAdmin)
admin.site.register(Cachorro, CachorroAdmin)
admin.site.register(Imagem, ImagemAdmin)
admin.site.register(Combinacao, CombinacaoAdmin)