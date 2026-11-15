from django.contrib import admin
from .models import Categoria, Mensagem

# Register your models here.




@admin.register(Categoria)                                       # ← novo
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "criada_em")          # ← + categoria
    list_filter = ("categoria",)                                 # ← novo filtro
    search_fields = ("titulo", "conteudo")
