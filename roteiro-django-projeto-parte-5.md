# Roteiro — Formulário HTML e o ciclo CRUD com Django

Esta é a **parte 5** do roteiro de evolução do projeto `demo-django`. Até aqui,
todo o cadastro de dados foi feito **pelo painel administrativo** ou pelo *shell*
do Django: o visitante comum só conseguia **ler** as mensagens na página inicial.

Nesta parte, vamos:

- Entender o conceito de **CRUD** e os métodos HTTP **GET** e **POST**.
- Criar um **formulário** com `ModelForm` para cadastrar mensagens.
- Escrever uma **view** que processa o formulário e salva no banco.
- Lidar com o campo **muitos-para-muitos** (`tags`) a partir de um texto digitado
  pelo visitante, criando as tags automaticamente.
- Proteger o formulário com **CSRF token** e aplicar o padrão **Post/Redirect/Get**.

Ao final, qualquer pessoa poderá **publicar uma mensagem com tags direto pela
página**, sem abrir o admin — fechando o **C** (Create) do ciclo CRUD do nosso app.

---

## 1. Executar e parar o projeto

Para **executar** o projeto:

```bash
docker compose up --build
```

Abra **http://localhost:8000** no navegador. Você deve ver a página inicial
listando as mensagens cadastradas nas partes anteriores, cada uma com título,
conteúdo, autor, categoria e tags.

Para **parar** o projeto:

`Ctrl+C` no terminal. Para remover o container:

```bash
docker compose down
```

> **Pré-requisito:** este roteiro pressupõe que você concluiu as partes
> [1](roteiro-django-projeto-inicial.md), [2](roteiro-django-projeto-parte-2.md),
> [3](roteiro-django-projeto-parte-3.md) e
> [4](roteiro-django-projeto-parte-4.md), nas quais o model `Mensagem` ganhou
> os campos `autor`, `categoria` (`ForeignKey`) e `tags` (`ManyToManyField`),
> além do model `Tag`.

---

## 2. Relembrando: o que é CRUD e onde estamos

**CRUD** é a sigla para as quatro operações básicas que quase toda aplicação faz
sobre os dados:

| Letra | Operação | Em português         | Já fazemos?                       |
|-------|----------|----------------------|-----------------------------------|
| **C** | Create   | Criar                | Só pelo admin / shell             |
| **R** | Read     | Ler / listar         | Sim — a página inicial lista    |
| **U** | Update   | Atualizar / editar   | Só pelo admin                     |
| **D** | Delete   | Apagar               | Só pelo admin                     |

Note que o **R** (Read) já está pronto desde a primeira parte: a `view` `index`
lê o banco e o template mostra a lista. O que falta é trazer o **C** (Create)
para a página pública. É isso que faremos agora.

> **GET vs POST:** o navegador conversa com o servidor por meio de
> *métodos HTTP*. Quando você **abre** uma página, o navegador faz um **GET**
> ("me mostre os dados"). Quando você **envia um formulário**, ele faz um
> **POST** ("guarde estes dados que estou mandando"). A mesma URL (`/nova/`)
> vai responder às duas situações: no GET ela **mostra o formulário em branco**;
> no POST ela **valida e salva** o que foi digitado.

---

## 3. Criar o formulário com `ModelForm`

O Django consegue gerar um formulário **a partir de um model**: ele olha os
campos da `Mensagem` e cria os campos de input correspondentes, com validação
automática. Essa classe especial se chama `ModelForm`.

Crie um arquivo novo chamado `home/forms.py` com o seguinte conteúdo:

```python
from django import forms

from .models import Mensagem

# Classe Tailwind reaproveitada por todos os campos do formulário.
INPUT = (
    "w-full rounded-lg bg-slate-800 border border-white/10 px-3 py-2 "
    "text-slate-100 focus:outline-none focus:ring-2 focus:ring-indigo-400"
)


class MensagemForm(forms.ModelForm):
    # Campo extra (não existe no model): o visitante digita as tags como texto
    # livre separado por vírgula. Vamos transformá-lo em objetos Tag na view.
    tags = forms.CharField(
        required=False,
        label="Tags",
        help_text="Separe por vírgula. Ex.: django, tutorial, iniciante",
        widget=forms.TextInput(attrs={"class": INPUT}),
    )

    class Meta:
        model = Mensagem
        fields = ["titulo", "conteudo", "autor", "categoria"]
        labels = {
            "titulo": "Título",
            "conteudo": "Conteúdo",
            "autor": "Autor",
            "categoria": "Categoria",
        }
        widgets = {
            "titulo": forms.TextInput(attrs={"class": INPUT}),
            "conteudo": forms.Textarea(attrs={"class": INPUT, "rows": 4}),
            "autor": forms.TextInput(attrs={"class": INPUT}),
            "categoria": forms.Select(attrs={"class": INPUT}),
        }
```

Pontos importantes:

- **`class Meta`** liga o formulário ao model `Mensagem` e diz **quais campos**
  entram no formulário. Repare que **não** incluímos `criada_em` (é preenchido
  sozinho por `auto_now_add`) nem `tags` na lista de `fields`.
- **Por que `tags` é declarado fora do `Meta`?** O campo `tags` do model é um
  `ManyToManyField`. Se o deixássemos no `fields`, o Django mostraria uma caixa
  de seleção múltipla apenas com as tags **já existentes** — o visitante não
  conseguiria criar tags novas. Por isso o substituímos por um `CharField` de
  texto livre, que processaremos manualmente na view.
- **`widgets`** customiza o HTML de cada campo. Aqui usamos isso só para aplicar
  as classes do Tailwind e transformar `conteudo` em uma `<textarea>` de 4 linhas.
- **`labels`** define os rótulos em português que aparecem acima de cada campo.

---

## 4. Criar a view que processa o formulário

Abra `home/views.py` e deixe-o assim:

```python
from django.shortcuts import redirect, render
from django.utils.text import slugify

from .forms import MensagemForm
from .models import Mensagem, Tag


def index(request):
    mensagens = Mensagem.objects.all()
    return render(request, "home/index.html", {"mensagens": mensagens})


def sobre(request):
    return render(request, "home/sobre.html")


def nova_mensagem(request):
    if request.method == "POST":
        form = MensagemForm(request.POST)
        if form.is_valid():
            # 1. Salva título, conteúdo, autor e categoria no banco.
            mensagem = form.save()

            # 2. Transforma o texto digitado em objetos Tag e associa à mensagem.
            tags_texto = form.cleaned_data["tags"]
            for pedaco in tags_texto.split(","):
                nome = slugify(pedaco)
                if nome:
                    tag, _ = Tag.objects.get_or_create(nome=nome)
                    mensagem.tags.add(tag)

            # 3. Redireciona para a página inicial (padrão Post/Redirect/Get).
            return redirect("index")
    else:
        form = MensagemForm()

    return render(request, "home/nova.html", {"form": form})
```

Vamos destrinchar a view `nova_mensagem`, que é o coração desta parte:

- **`if request.method == "POST"`** — separa os dois cenários explicados na
  seção 2. Se for POST, o visitante enviou o formulário; caso contrário (GET),
  só queremos mostrar o formulário em branco.
- **`MensagemForm(request.POST)`** — cria o formulário **preenchido** com os
  dados que vieram do navegador.
- **`form.is_valid()`** — roda toda a validação automática (campos obrigatórios,
  tamanho máximo, etc.). Se algo estiver errado, o `if` é falso e caímos no
  `render` final, que mostra o formulário **com as mensagens de erro**.
- **`form.save()`** — grava a nova `Mensagem` na tabela `home_mensagem` e
  devolve o objeto salvo. Como `tags` **não** está no `fields` do formulário,
  ele não é tocado aqui — cuidamos dele no passo seguinte.
- **`slugify(pedaco)`** — converte cada pedaço de texto em um *slug* válido
  (`"Tutorial Django"` vira `"tutorial-django"`), exatamente o formato exigido
  pelo `SlugField` da tag. O `if nome:` descarta pedaços vazios (por exemplo,
  quando o visitante digita `"django, "` com uma vírgula sobrando).
- **`Tag.objects.get_or_create(nome=nome)`** — **busca** a tag pelo nome; se ela
  não existir, **cria** na hora. É isso que permite ao visitante inventar tags
  novas. O método devolve uma tupla `(objeto, criado?)`; usamos `_` para ignorar
  o segundo valor, que não nos interessa.
- **`mensagem.tags.add(tag)`** — adiciona uma linha na tabela de junção
  `home_mensagem_tags`, associando a tag à mensagem.

> **Padrão Post/Redirect/Get (PRG):** depois de salvar, fazemos
> `return redirect("index")` em vez de renderizar uma página direto. Isso evita
> o clássico problema de "recarreguei a página e a mensagem foi enviada de novo":
> após o POST, o navegador é mandado fazer um **GET** limpo na página inicial.
> O nome `"index"` é o que definimos em `name="index"` no `urls.py`.

---

## 5. Registrar a rota

Abra `home/urls.py` e acrescente o caminho da nova página:

```python
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sobre/", views.sobre, name="sobre"),
    path("nova/", views.nova_mensagem, name="nova_mensagem"),   # ← novo
]
```

Agora a URL **http://localhost:8000/nova/** está ligada à view `nova_mensagem`.

---

## 6. Criar o template do formulário

Crie um arquivo novo chamado `templates/home/nova.html`:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nova mensagem — Demo Django</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900 min-h-screen text-slate-100">

    <header class="container mx-auto px-6 py-12">
        <nav class="flex items-center justify-between">
            <div class="flex items-center gap-2">
                <span class="w-3 h-3 rounded-full bg-emerald-400 animate-pulse"></span>
                <span class="font-mono text-sm text-slate-300">demo-django</span>
            </div>
            <a href="/" class="text-sm text-slate-300 hover:text-white transition">← voltar</a>
        </nav>
    </header>

    <main class="container mx-auto px-6 py-12">
        <section class="bg-white/5 backdrop-blur border border-white/10 rounded-xl p-8 max-w-2xl">
            <h1 class="text-2xl font-bold mb-6">Publicar uma mensagem</h1>

            <form method="post" action="{% url 'nova_mensagem' %}" class="space-y-5">
                {% csrf_token %}

                {% for field in form %}
                    <div>
                        <label for="{{ field.id_for_label }}" class="block text-sm font-medium text-slate-300 mb-1">
                            {{ field.label }}
                        </label>
                        {{ field }}
                        {% if field.help_text %}
                            <p class="text-xs text-slate-500 mt-1">{{ field.help_text }}</p>
                        {% endif %}
                        {% for erro in field.errors %}
                            <p class="text-xs text-red-400 mt-1">{{ erro }}</p>
                        {% endfor %}
                    </div>
                {% endfor %}

                <button type="submit"
                        class="px-5 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-900 font-semibold transition">
                    Publicar
                </button>
            </form>
        </section>
    </main>

    <footer class="container mx-auto px-6 py-12 text-center text-slate-500 text-sm">
        Feito para a aula de Programação Web · Django {{ '5.1' }}
    </footer>

</body>
</html>
```

Detalhes que merecem atenção:

- **`<form method="post" action="{% url 'nova_mensagem' %}">`** — o `method="post"`
  faz o navegador **enviar** os dados (e não apenas pedir a página). A tag
  `{% url 'nova_mensagem' %}` gera a URL `/nova/` a partir do `name` da rota,
  evitando deixar o caminho "chumbado" no HTML.
- **`{% csrf_token %}`** — **obrigatório** em todo formulário POST do Django.
  Ele insere um campo escondido com um *token* de segurança que protege contra
  ataques **CSRF** (Cross-Site Request Forgery). Se você esquecer essa linha,
  o Django responde com um erro **403 Forbidden** ao enviar o formulário.
- **`{% for field in form %}`** — em vez de escrever o HTML de cada campo na mão,
  percorremos o formulário e o Django renderiza cada `input`/`textarea`/`select`
  para nós (já com as classes Tailwind que definimos nos `widgets`).
- **`{{ field.errors }}`** — quando a validação falha, as mensagens de erro
  aparecem em vermelho logo abaixo do campo problemático.

---

## 7. Criar o link para o formulário na página inicial

Para o visitante encontrar o formulário, abra `templates/home/index.html` e,
dentro da seção "Mensagens do banco de dados", logo após o parágrafo de
instruções, acrescente um botão:

```html
<a href="/nova/"
   class="inline-block mb-6 px-4 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-900 font-semibold transition">
    + Nova mensagem
</a>
```

Você pode posicioná-lo logo antes do `{% if mensagens %}`.

---

## 8. Testar o ciclo completo

Com o projeto rodando (`docker compose up`), faça o teste de ponta a ponta:

1. Acesse **http://localhost:8000/** e clique em **+ Nova mensagem**.
2. Preencha título, conteúdo, autor, escolha uma categoria e digite algumas
   tags separadas por vírgula — por exemplo: `django, formulário, iniciante`.
3. Clique em **Publicar**.
4. Você será redirecionado para a página inicial e verá **a sua mensagem no
   topo da lista** (lembre-se de que o model ordena por `-criada_em`), já com
   o selo da categoria e as tags exibidas com `#`.

Experimente também os casos de **validação**:

- Deixe o **título em branco** e tente publicar: o formulário recarrega com a
  mensagem de erro em vermelho, sem salvar nada no banco.
- Publique duas mensagens usando a tag `django`: a tag é **reaproveitada** (não
  duplica), graças ao `get_or_create`. Confira em
  **http://localhost:8000/admin/** → **Tags**.

> **Conferindo no banco (opcional):**
> ```bash
> docker compose exec web python manage.py shell
> ```
> ```python
> >>> from home.models import Mensagem
> >>> m = Mensagem.objects.first()      # a mais recente
> >>> m.titulo
> >>> m.tags.all()                       # as tags que você digitou
> ```

---

## 9. (Opcional) Dar um retorno visual com o framework de *messages*

Hoje, ao publicar, o visitante é levado de volta à home mas **não recebe nenhum
aviso** de que deu certo. O Django tem um sistema pronto de mensagens
temporárias (*flash messages*) para isso.

Na view, importe e use `messages`:

```python
from django.contrib import messages
# ...

        if form.is_valid():
            mensagem = form.save()
            # ... laço das tags ...
            messages.success(request, "Mensagem publicada com sucesso!")
            return redirect("index")
```

E no `templates/home/index.html`, logo no início do `<main>`, exiba os avisos:

```html
{% if messages %}
    {% for message in messages %}
        <div class="max-w-3xl mb-6 px-4 py-3 rounded-lg bg-emerald-500/20 text-emerald-200 text-sm">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}
```

O aviso aparece **uma única vez** após o redirecionamento e some ao recarregar
a página — comportamento típico de *flash message*.

---

Você acabou de implementar o **C** (Create) do CRUD com um formulário
público, juntando quase tudo que viu nas partes anteriores: model, relacionamentos
`ForeignKey` e `ManyToManyField`, template e, agora, **views que processam dados
enviados pelo usuário** com validação e segurança contra CSRF.

No próximo roteiro, vamos completar o ciclo implementando o **U** (Update) e o
**D** (Delete): páginas para **editar** e **apagar** uma mensagem existente,
reaproveitando o mesmo `MensagemForm` e aprendendo a passar o `id` da mensagem
pela URL.
