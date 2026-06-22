# Roteiro — Criando modelos e relacionamento com DJango

Esta é a continuação do roteiro para você construir, do zero, o projeto
`demo-django`: um site simples de uma página, escrito em **Django**, estilizado
com **Tailwind CSS** (via CDN), salvando dados em **SQLite** e executado dentro
de um container **Docker**.

Nesta roteiro, você terá uma página inicial que lista mensagens cadastradas no banco
através do painel administrativo do Django.

---

## 1. Executar e parar o projeto

Para **executar** o projeto:

```bash
docker compose up --build
```

Isso vai:

1. Construir a imagem (só na primeira vez, ou quando o `Dockerfile` mudar).
2. Aplicar as migrations no SQLite (`db.sqlite3` é criado).
3. Iniciar o servidor em `http://localhost:8000`.

Abra **http://localhost:8000** no navegador. Você deve ver a página com o
cabeçalho "Olá, Django + Tailwind!" e a seção dizendo "Nenhuma mensagem ainda."

Para contruir essa página, você deve executar o [roteiro anterior](roteiro-django-projeto-inicial.md).

Para **parar** o projeto:

`Ctrl+C` no terminal. Para remover o container:

```bash
docker compose down
```

## 2. Criar um novo model com relacionamento

Até aqui, nosso banco tem uma única tabela: `home_mensagem`. Nesta seção, você
vai criar uma **segunda tabela** — `home_categoria` — e ligar cada mensagem a
uma categoria. Esse é o tipo de relacionamento mais comum em aplicações reais
(um cliente tem vários pedidos, um post tem vários comentários, etc.).

> **Conceito:** essa relação se chama **um-para-muitos** (1:N). *Uma* categoria
> pode estar associada a *várias* mensagens, mas cada mensagem pertence a
> *apenas uma* categoria. No Django, isso é representado por um campo
> `ForeignKey` no lado "muitos" (na `Mensagem`).

### Passo 1 — Criar o model `Categoria` e ligar a `Mensagem`

Abra `home/models.py` e deixe-o assim:

```python
from django.db import models


class Categoria(models.Model):                                  # ← novo model
    nome = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Mensagem(models.Model):
    titulo = models.CharField(max_length=120)
    conteudo = models.TextField()
    autor = models.CharField(max_length=80, default="Anônimo")
    categoria = models.ForeignKey(                              # ← novo campo
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mensagens",
    )
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criada_em"]

    def __str__(self):
        return self.titulo
```

O que cada parâmetro do `ForeignKey` significa:

- `Categoria` → a tabela "do outro lado" da relação.
- `on_delete=models.SET_NULL` → se uma categoria for apagada, as mensagens
  dela **não** são apagadas; o campo `categoria` simplesmente vira `NULL`.
- `null=True, blank=True` → permite mensagens sem categoria (útil para as
  mensagens que já existem no banco e ainda não foram classificadas).
- `related_name="mensagens"` → cria o atalho `categoria.mensagens.all()`
  para listar todas as mensagens de uma categoria (usaremos no Passo 5).

### Passo 2 — Registrar `Categoria` no admin

Abra `home/admin.py` e acrescente o registro:

```python
from django.contrib import admin

from .models import Categoria, Mensagem


@admin.register(Categoria)                                       # ← novo
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)


@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin):
    list_display = ("titulo", "categoria", "criada_em")          # ← + categoria
    list_filter = ("categoria",)                                 # ← novo filtro
    search_fields = ("titulo", "conteudo")
```

### Passo 3 — Gerar e aplicar a migration

```bash
docker compose run --rm web python manage.py makemigrations
docker compose run --rm web python manage.py migrate
```

Saída esperada do `makemigrations`:

```
Migrations for 'home':
  home/migrations/0003_categoria_mensagem_categoria.py
    + Create model Categoria
    + Add field categoria to mensagem
```

E o `migrate` termina com `Applying home.0003_... OK`. Agora o SQLite tem
**duas** tabelas: `home_categoria` e `home_mensagem` (esta última com a
coluna `categoria_id` apontando para a primeira).

> **Conferindo no banco (opcional):**
> ```bash
> docker compose exec web python manage.py dbshell
> sqlite> .tables
> sqlite> .schema home_mensagem
> sqlite> .quit
> ```
> Você verá a coluna `categoria_id INTEGER REFERENCES "home_categoria"("id")`.

### Passo 4 — Cadastrar categorias e associar mensagens no admin

1. Acesse **http://localhost:8000/admin/**.
2. Clique em **Categorias → Adicionar** e crie, por exemplo, "Aviso",
   "Dúvida" e "Sugestão".
3. Volte em **Mensagens**, edite uma mensagem existente e selecione uma
   categoria no menu suspenso. Salve.
4. Na lista de mensagens, a coluna `Categoria` agora aparece preenchida e
   o filtro à direita permite filtrar por categoria.

### Passo 5 — Exibir a categoria no template

Em `templates/home/index.html`, dentro do `{% for m in mensagens %}`,
acrescente o "selo" da categoria:

```html
<li class="border-l-2 border-emerald-400 pl-4 py-1">
    <h3 class="font-semibold">{{ m.titulo }}</h3>
    {% if m.categoria %}
        <span class="inline-block px-2 py-0.5 mt-1 bg-indigo-500/20 text-indigo-300 text-xs rounded-full">
            {{ m.categoria.nome }}
        </span>
    {% endif %}
    <p class="text-sm text-slate-300">{{ m.conteudo }}</p>
    <span class="text-xs text-slate-400">por {{ m.autor }}</span>
    <span class="text-xs text-slate-500">{{ m.criada_em|date:"d/m/Y H:i" }}</span>
</li>
```

Observe o `{% if m.categoria %}`: ele protege o template caso a mensagem
ainda não tenha categoria associada (lembre-se de que permitimos `null=True`).

Para acessar um campo da tabela relacionada, basta usar `.`: a expressão
`{{ m.categoria.nome }}` significa "a partir da mensagem `m`, vá até a
`categoria` ligada a ela e pegue o `nome`". Por trás dos panos, o Django faz
um `JOIN` no SQL para buscar o registro correspondente em `home_categoria`.

### Passo 6 (opcional) — Usar o relacionamento inverso

Como definimos `related_name="mensagens"`, o caminho contrário também
funciona. Abra o shell do Django para experimentar:

```bash
docker compose exec web python manage.py shell
```

```python
>>> from home.models import Categoria
>>> c = Categoria.objects.get(nome="Aviso")
>>> c.mensagens.all()              # todas as mensagens dessa categoria
>>> c.mensagens.count()            # quantas mensagens existem nessa categoria
```

Esse acesso reverso é o que torna o ORM do Django tão produtivo: você modela
a relação **uma vez** e navega nela nos dois sentidos.

