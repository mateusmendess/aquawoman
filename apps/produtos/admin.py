from django.contrib import admin
from .models import Categoria, Produto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'icone', 'ativo']
    prepopulated_fields = {'slug': ('nome',)}
    list_editable = ['ativo']

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'preco', 'estoque', 'ativo', 'destaque']
    prepopulated_fields = {'slug': ('nome',)}
    list_editable = ['ativo', 'destaque', 'preco', 'estoque']
    list_filter = ['categoria', 'ativo', 'destaque']
    search_fields = ['nome', 'descricao']