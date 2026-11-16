from django.contrib import admin

from .models import Categoria, Mensagem, Tag


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


@admin.register(Tag)                                            # ← novo
class TagAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "criada_em")
    list_filter = ("categoria", "tags")                         # ← + tags
    search_fields = ("titulo", "conteudo")
    filter_horizontal = ("tags",)                               # ← novo