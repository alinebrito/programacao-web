# Roteiro —  Criando modelos e relacionamento muitos-para-muitos com DJango

Esta é a **parte 4** do roteiro de evolução do projeto `demo-django`. Nas etapas
anteriores você criou o app, registrou mensagens pelo painel administrativo,
adicionou um campo novo a um model e criou um relacionamento **um-para-muitos**
(`Mensagem` → `Categoria`) usando `ForeignKey`.

Nesta parte, vamos aprender:

- Como criar um relacionamento **muitos-para-muitos** (N:N) — diferente do
  `ForeignKey` da parte anterior.
- Como **inserir dados no banco diretamente pelo Django**, usando o *shell*
  interativo e a API do ORM (sem precisar abrir o painel admin a cada vez).

Ao final, sua aplicação terá uma nova tabela `home_tag`, cada mensagem poderá
estar associada a **várias** tags (e cada tag a várias mensagens), e você terá
populado essa estrutura escrevendo código Python — exatamente como um script de
*seed* faria em um projeto real.

---

## 1. Executar e parar o projeto

Para **executar** o projeto:

```bash
docker compose up --build
```

Abra **http://localhost:8000** no navegador. Você deve ver a página inicial com
as mensagens já cadastradas nas partes anteriores do roteiro, cada uma exibindo
título, conteúdo, autor e (se já associada) categoria.

Para **parar** o projeto:

`Ctrl+C` no terminal. Para remover o container:

```bash
docker compose down
```

> **Pré-requisito:** este roteiro pressupõe que você concluiu as partes
> [1](roteiro-django-projeto-inicial.md), [2](roteiro-django-projeto-parte-2.md)
> e [3](roteiro-django-projeto-parte-3.md), nas quais o model `Mensagem` ganhou
> os campos `autor`, `categoria` (`ForeignKey`) e o admin foi configurado.

---

## 2. Recapitulando: onde estamos

Antes de avançar, abra o arquivo `home/models.py` e confirme que ele está mais
ou menos assim:

```python
from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Mensagem(models.Model):
    titulo = models.CharField(max_length=120)
    conteudo = models.TextField()
    autor = models.CharField(max_length=80, default="Anônimo")
    categoria = models.ForeignKey(
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

Hoje o banco tem **duas tabelas relacionadas**:

```
home_categoria (1)  ───<  home_mensagem (N)
```

Uma categoria pode ter várias mensagens, mas cada mensagem só pode estar em uma
categoria. Esse é o relacionamento **um-para-muitos**.

Agora pense no seguinte cenário: a mesma mensagem pode falar de "django",
"tutorial" e "iniciante" ao mesmo tempo. E essas palavras-chave também aparecem
em **outras** mensagens. Aqui o `ForeignKey` não serve — precisamos de uma
relação **muitos-para-muitos**.

---

## 3. Criar um relacionamento muitos-para-muitos

> **Conceito:** em um relacionamento **muitos-para-muitos** (N:N), os dois
> lados podem se conectar a vários registros do outro. No banco, isso é
> implementado por uma **tabela intermediária** (também chamada de *tabela de
> junção*) que guarda os pares `(mensagem_id, tag_id)`. O Django cria essa
> tabela automaticamente para você quando você usa `ManyToManyField`.

### Passo 1 — Criar o model `Tag` e o campo `tags` em `Mensagem`

Abra `home/models.py` e edite-o para ficar assim (note as duas linhas
marcadas com `# ← novo`):

```python
from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Tag(models.Model):                                        # ← novo model
    nome = models.SlugField(max_length=30, unique=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Mensagem(models.Model):
    titulo = models.CharField(max_length=120)
    conteudo = models.TextField()
    autor = models.CharField(max_length=80, default="Anônimo")
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mensagens",
    )
    tags = models.ManyToManyField(                              # ← novo campo
        Tag,
        blank=True,
        related_name="mensagens",
    )
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criada_em"]

    def __str__(self):
        return self.titulo
```

Algumas observações importantes:

- **`SlugField`** em vez de `CharField`: garante que o nome da tag fique no
  formato de "URL amigável" (só letras, números, hífens e *underscore*). Assim
  evitamos tags com espaços ou acentos, que tendem a quebrar links.
- **`unique=True`**: duas tags não podem ter o mesmo nome.
- **`ManyToManyField(Tag, blank=True)`**: o `blank=True` permite salvar uma
  mensagem **sem nenhuma tag** pelo admin (note que aqui **não usamos**
  `null=True` — `ManyToManyField` ignora esse parâmetro porque a relação
  vazia é representada simplesmente pela ausência de linhas na tabela de
  junção, não por um `NULL`).
- **`related_name="mensagens"`**: cria o atalho `tag.mensagens.all()` para
  listar todas as mensagens com aquela tag.

### Passo 2 — Registrar `Tag` no admin e mostrar tags na lista de mensagens

Abra `home/admin.py` e deixe-o assim:

```python
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
```

> **O que faz `filter_horizontal`?** Por padrão, o admin mostra um campo de
> seleção múltipla horroroso (aquele `<select multiple>` minúsculo) para campos
> `ManyToManyField`. Com `filter_horizontal = ("tags",)` o Django troca por
> dois painéis lado a lado ("disponíveis" / "escolhidas") muito mais
> confortáveis de usar.

### Passo 3 — Gerar e aplicar a migration

No terminal, na mesma pasta do `docker-compose.yml`:

```bash
docker compose run --rm web python manage.py makemigrations
docker compose run --rm web python manage.py migrate
```

A saída esperada do `makemigrations` é parecida com:

```
Migrations for 'home':
  home/migrations/0004_tag_mensagem_tags.py
    + Create model Tag
    + Add field tags to mensagem
```

E o `migrate` termina com `Applying home.0004_... OK`.

> **O que acabou de acontecer no SQLite?** Foram criadas **duas** tabelas
> novas: `home_tag` (com `id` e `nome`) e `home_mensagem_tags` (a tabela de
> junção, com apenas duas colunas: `mensagem_id` e `tag_id`). Você nunca
> precisa manipular `home_mensagem_tags` diretamente — o Django faz isso por
> você quando você chama `mensagem.tags.add(...)` no Passo 4 da próxima seção.

### Passo 4 (opcional) — Conferir as tabelas no SQLite

```bash
docker compose exec web python manage.py dbshell
sqlite> .tables
sqlite> .schema home_mensagem_tags
sqlite> .quit
```

Você deve ver `home_mensagem_tags` com a estrutura:

```sql
CREATE TABLE "home_mensagem_tags" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "mensagem_id" bigint NOT NULL REFERENCES "home_mensagem" ("id") ...,
    "tag_id" bigint NOT NULL REFERENCES "home_tag" ("id") ...
);
```

Cada linha dessa tabela é **uma associação** entre uma mensagem e uma tag.
Se uma mensagem tem 3 tags, existem 3 linhas com o mesmo `mensagem_id`.

---

## 5. Exibir as tags no template

Abra `templates/home/index.html` e, dentro do `{% for m in mensagens %}`,
acrescente o bloco que exibe as tags. Substitua o `<li>` atual por:

```html
<li class="border-l-2 border-emerald-400 pl-4 py-1">
    <h3 class="font-semibold">{{ m.titulo }}</h3>
    {% if m.categoria %}
        <span class="inline-block px-2 py-0.5 mt-1 bg-indigo-500/20 text-indigo-300 text-xs rounded-full">
            {{ m.categoria.nome }}
        </span>
    {% endif %}
    <p class="text-sm text-slate-300">{{ m.conteudo }}</p>
    {% if m.tags.all %}                                          {# ← novo #}
        <div class="flex flex-wrap gap-1 mt-1">
            {% for tag in m.tags.all %}
                <span class="inline-block px-2 py-0.5 bg-emerald-500/15 text-emerald-300 text-xs rounded">
                    #{{ tag.nome }}
                </span>
            {% endfor %}
        </div>
    {% endif %}
    <span class="text-xs text-slate-400">por {{ m.autor }}</span>
    <span class="text-xs text-slate-500">{{ m.criada_em|date:"d/m/Y H:i" }}</span>
</li>
```

Pontos importantes desse trecho:

- **`{% if m.tags.all %}`** evita renderizar a `<div>` vazia quando a mensagem
  não tem nenhuma tag — algo essencial porque algumas mensagens antigas
  podem nunca ter recebido tag alguma.
- **`{% for tag in m.tags.all %}`** percorre o `QuerySet` retornado pelo
  campo `ManyToManyField`. Cada iteração `tag` é uma instância do model `Tag`.
- O `#` antes de `{{ tag.nome }}` é só um detalhe visual, lembrando o estilo
  de *hashtag* das redes sociais.

Recarregue **http://localhost:8000/** e veja as tags aparecendo abaixo do
conteúdo da mensagem.


No próximo roteiro, vamos sair do admin e do shell e criar um **formulário
HTML** que permita ao próprio visitante publicar uma mensagem com tags
direto pela página — fechando o ciclo CRUD (Create-Read-Update-Delete) do
nosso app.
