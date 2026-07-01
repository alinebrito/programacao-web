# Roteiro — Editar e remover: finalizando o ciclo CRUD com Django

Esta é a **parte 6** do roteiro de evolução do projeto `demo-django`. Na
[parte 5](roteiro-django-projeto-parte-5.md) você criou um formulário público
e trouxe o **C** (Create) do CRUD para a página, permitindo que qualquer
visitante publicasse uma mensagem com tags.

Faltam as duas últimas letras:

| Letra | Operação | Em português       | Status                          |
|-------|----------|--------------------|---------------------------------|
| **C** | Create   | Criar              | feito na parte 5             |
| **R** | Read     | Ler / listar       | feito desde a parte 1        |
| **U** | Update   | Atualizar / editar | **faremos agora**            |
| **D** | Delete   | Apagar             | **faremos agora**            |

Nesta parte, vamos:

- Aprender a **passar o `id` de um registro pela URL** (parâmetros de rota).
- Usar `get_object_or_404` para **buscar uma mensagem** com segurança.
- **Reaproveitar o `MensagemForm`** para editar uma mensagem já existente.
- Criar uma **página de confirmação** antes de apagar.
- Entender por que toda **exclusão deve acontecer via POST**, nunca via GET.

Ao final, o ciclo **CRUD estará completo**: o visitante poderá criar, listar,
**editar** e **remover** mensagens sem nunca abrir o painel admin.

---

## 1. Executar e parar o projeto

Para **executar** o projeto:

```bash
docker compose up --build
```

Abra **http://localhost:8000** no navegador. Você deve ver a lista de mensagens
e o botão **+ Nova mensagem** criado na parte anterior.

Para **parar** o projeto:

`Ctrl+C` no terminal. Para remover o container:

```bash
docker compose down
```

> **Pré-requisito:** este roteiro pressupõe que você concluiu a
> [parte 5](roteiro-django-projeto-parte-5.md), na qual foram criados o
> `MensagemForm` (em `home/forms.py`), a view `nova_mensagem`, a rota `nova/`
> e o template `home/nova.html`.

---

## 2. Conceito: passar o `id` pela URL

Para editar ou remover uma mensagem, o servidor precisa saber **qual** delas.
Cada registro no banco tem um identificador único — o campo `id`, criado
automaticamente pelo Django. Vamos colocá-lo **dentro da URL**:

```
/mensagens/7/editar/      → editar a mensagem de id 7
/mensagens/7/remover/     → remover a mensagem de id 7
```

> **Conceito — parâmetros de rota:** no `urls.py`, o trecho `<int:id>` é um
> *conversor de caminho* (*path converter*). Ele captura o número que aparece
> naquela posição da URL, garante que é um inteiro e o entrega para a view como
> um argumento chamado `id`. Assim, a mesma view atende a `/mensagens/7/editar/`,
> `/mensagens/42/editar/` e assim por diante.

---

## 3. Editar uma mensagem (Update)

A grande sacada aqui é **reaproveitar o `MensagemForm`** da parte 5. O mesmo
formulário que cria uma mensagem também consegue editá-la — basta dizer a ele
**qual instância** estamos modificando, por meio do parâmetro `instance`.

### Passo 1 — Extrair a lógica das tags para uma função

Na parte 5, a view `nova_mensagem` continha um trecho que transforma o texto
digitado em objetos `Tag`. Como a edição vai precisar **exatamente da mesma
lógica**, vamos evitar copiar e colar: extraímos esse trecho para uma função
reutilizável (princípio **DRY** — *Don't Repeat Yourself*).

Abra `home/views.py` e deixe-o assim:

```python
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from .forms import MensagemForm
from .models import Mensagem, Tag


def _aplicar_tags(mensagem, tags_texto):
    """Substitui as tags da mensagem pelas que vieram do formulário."""
    mensagem.tags.clear()
    for pedaco in tags_texto.split(","):
        nome = slugify(pedaco)
        if nome:
            tag, _ = Tag.objects.get_or_create(nome=nome)
            mensagem.tags.add(tag)


def index(request):
    mensagens = Mensagem.objects.all()
    return render(request, "home/index.html", {"mensagens": mensagens})


def sobre(request):
    return render(request, "home/sobre.html")


def nova_mensagem(request):
    if request.method == "POST":
        form = MensagemForm(request.POST)
        if form.is_valid():
            mensagem = form.save()
            _aplicar_tags(mensagem, form.cleaned_data["tags"])
            messages.success(request, "Mensagem publicada com sucesso!")
            return redirect("index")
    else:
        form = MensagemForm()

    return render(request, "home/nova.html", {"form": form})


def editar_mensagem(request, id):
    mensagem = get_object_or_404(Mensagem, id=id)

    if request.method == "POST":
        form = MensagemForm(request.POST, instance=mensagem)
        if form.is_valid():
            mensagem = form.save()
            _aplicar_tags(mensagem, form.cleaned_data["tags"])
            messages.success(request, "Mensagem atualizada com sucesso!")
            return redirect("index")
    else:
        tags_atuais = ", ".join(tag.nome for tag in mensagem.tags.all())
        form = MensagemForm(instance=mensagem, initial={"tags": tags_atuais})

    return render(request, "home/editar.html", {"form": form, "mensagem": mensagem})
```

> **Nota:** repare que a `nova_mensagem` ficou mais curta — agora ela chama
> `_aplicar_tags(...)` em vez de repetir o laço. O `mensagem.tags.clear()` no
> início da função é inofensivo quando a mensagem acabou de ser criada (ela
> ainda não tem tags), e é **essencial** na edição, como veremos a seguir.

Entendendo a view `editar_mensagem`:

- **`get_object_or_404(Mensagem, id=id)`** — busca a mensagem com aquele `id`.
  Se ela não existir (por exemplo, alguém digitou `/mensagens/9999/editar/`),
  o Django responde com a página **404 (não encontrado)** automaticamente, em
  vez de quebrar com um erro.
- **`MensagemForm(request.POST, instance=mensagem)`** — no POST, o `instance`
  diz ao formulário "não crie uma mensagem nova; **atualize esta aqui**". O
  `form.save()` então faz um `UPDATE` no banco, e não um `INSERT`.
- **`MensagemForm(instance=mensagem, initial={...})`** — no GET, o `instance`
  preenche os campos do formulário com os **valores atuais** da mensagem. Como
  o campo `tags` é de texto livre (não vem do model), preenchemos seu valor
  inicial à parte, juntando as tags atuais com vírgula em `tags_atuais`.
- **`mensagem.tags.clear()`** (dentro de `_aplicar_tags`) — na edição, primeiro
  **removemos todas as associações antigas** e depois recriamos a partir do que
  está no formulário. Sem isso, editar a mensagem só **acrescentaria** tags,
  nunca removeria as que o usuário apagou do campo.

### Passo 2 — Registrar a rota de edição

Abra `home/urls.py` e acrescente o caminho com o parâmetro `<int:id>`:

```python
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sobre/", views.sobre, name="sobre"),
    path("nova/", views.nova_mensagem, name="nova_mensagem"),
    path("mensagens/<int:id>/editar/", views.editar_mensagem, name="editar_mensagem"),   # ← novo
]
```

### Passo 3 — Criar o template de edição

Crie um arquivo novo chamado `templates/home/editar.html`. Ele é quase idêntico
ao `nova.html`, mudando apenas o título, o texto do botão e o `action` do
formulário (que agora aponta para a rota de edição, passando o `id`):

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editar mensagem — Demo Django</title>
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
            <h1 class="text-2xl font-bold mb-6">Editar mensagem</h1>

            <form method="post" action="{% url 'editar_mensagem' mensagem.id %}" class="space-y-5">
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
                    Salvar alterações
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

A única diferença conceitual em relação ao `nova.html` é o `action`:
`{% url 'editar_mensagem' mensagem.id %}` gera, por exemplo, `/mensagens/7/editar/`.
É por isso que passamos `mensagem` no contexto da view — o template precisa do
`id` para montar essa URL.

---

## 4. Remover uma mensagem (Delete)

Apagar dados é uma ação **destrutiva e irreversível**. Por isso, faremos em
duas etapas: o visitante clica em "Remover", cai numa **página de confirmação**,
e só ao confirmar (enviando um POST) a mensagem é de fato apagada.

> **Por que nunca apagar no GET?** Um GET deveria apenas **ler** dados, sem
> efeitos colaterais. Se a exclusão acontecesse ao simplesmente *abrir* uma URL
> como `/mensagens/7/remover/`, qualquer coisa que "visite" links — o
> pré-carregamento do navegador, um robô de busca, um antivírus — poderia
> **apagar registros sem ninguém clicar em nada**. Por isso a remoção real só
> ocorre via **POST**, protegida pelo `{% csrf_token %}`.

### Passo 1 — Criar a view de remoção

Acrescente ao final de `home/views.py`:

```python
def remover_mensagem(request, id):
    mensagem = get_object_or_404(Mensagem, id=id)

    if request.method == "POST":
        mensagem.delete()
        messages.success(request, "Mensagem removida.")
        return redirect("index")

    return render(request, "home/remover.html", {"mensagem": mensagem})
```

- No **GET**, a view apenas mostra a página de confirmação (`remover.html`).
- No **POST** (quando o visitante confirma), `mensagem.delete()` apaga a linha
  da tabela `home_mensagem`. As associações na tabela de junção
  `home_mensagem_tags` somem junto automaticamente; as **tags em si**
  (`home_tag`) continuam existindo, pois podem ser usadas por outras mensagens.

### Passo 2 — Registrar a rota de remoção

Em `home/urls.py`, acrescente:

```python
    path("mensagens/<int:id>/remover/", views.remover_mensagem, name="remover_mensagem"),  # ← novo
```

O `urlpatterns` completo fica assim:

```python
urlpatterns = [
    path("", views.index, name="index"),
    path("sobre/", views.sobre, name="sobre"),
    path("nova/", views.nova_mensagem, name="nova_mensagem"),
    path("mensagens/<int:id>/editar/", views.editar_mensagem, name="editar_mensagem"),
    path("mensagens/<int:id>/remover/", views.remover_mensagem, name="remover_mensagem"),
]
```

### Passo 3 — Criar o template de confirmação

Crie `templates/home/remover.html`:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Remover mensagem — Demo Django</title>
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
            <h1 class="text-2xl font-bold mb-4">Remover mensagem</h1>
            <p class="text-slate-300 mb-6">
                Tem certeza de que deseja remover a mensagem
                <strong>"{{ mensagem.titulo }}"</strong>? Esta ação não pode ser desfeita.
            </p>

            <form method="post" action="{% url 'remover_mensagem' mensagem.id %}" class="flex items-center gap-3">
                {% csrf_token %}
                <button type="submit"
                        class="px-5 py-2 rounded-lg bg-red-500 hover:bg-red-400 text-white font-semibold transition">
                    Sim, remover
                </button>
                <a href="/" class="px-5 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-slate-200 transition">
                    Cancelar
                </a>
            </form>
        </section>
    </main>

    <footer class="container mx-auto px-6 py-12 text-center text-slate-500 text-sm">
        Feito para a aula de Programação Web · Django {{ '5.1' }}
    </footer>

</body>
</html>
```

Note que o botão **"Sim, remover"** está dentro de um `<form method="post">`
(dispara o POST que apaga), enquanto **"Cancelar"** é apenas um link comum
(`<a href="/">`) que leva de volta à home sem apagar nada.

---

## 5. Adicionar os botões "Editar" e "Remover" na lista

Agora ligamos tudo na página inicial. Abra `templates/home/index.html` e, dentro
do `{% for m in mensagens %}`, acrescente os dois links ao final de cada `<li>`,
logo após a data:

```html
<li class="border-l-2 border-emerald-400 pl-4 py-1">
    <h3 class="font-semibold">{{ m.titulo }}</h3>
    {% if m.categoria %}
        <span class="inline-block px-2 py-0.5 mt-1 bg-indigo-500/20 text-indigo-300 text-xs rounded-full">
            {{ m.categoria.nome }}
        </span>
    {% endif %}
    <p class="text-sm text-slate-300">{{ m.conteudo }}</p>
    {% if m.tags.all %}
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

    <div class="flex gap-3 mt-1">                                            {# ← novo #}
        <a href="{% url 'editar_mensagem' m.id %}"
           class="text-xs text-indigo-300 hover:text-indigo-200 underline">editar</a>
        <a href="{% url 'remover_mensagem' m.id %}"
           class="text-xs text-red-400 hover:text-red-300 underline">remover</a>
    </div>
</li>
```

A tag `{% url 'editar_mensagem' m.id %}` monta a URL de cada mensagem usando o
`name` da rota e o `id` daquela mensagem do laço — exatamente o que a view
espera receber no parâmetro `id`.

---

## 6. Testar o ciclo CRUD completo

Com o projeto rodando (`docker compose up`), percorra todo o ciclo pela página,
**sem abrir o admin**:

1. **Create** — clique em **+ Nova mensagem**, preencha e publique. Ela aparece
   no topo da lista.
2. **Read** — confira que a mensagem aparece com título, categoria e tags.
3. **Update** — clique em **editar** na mensagem recém-criada. O formulário
   abre **já preenchido**, inclusive com as tags no campo de texto. Mude o
   título, **apague uma das tags** e salve. Confirme que a alteração (e a
   remoção da tag) apareceu na lista.
4. **Delete** — clique em **remover**. Na página de confirmação, clique em
   **Cancelar** e veja que nada acontece. Clique em **remover** de novo e
   confirme em **Sim, remover**: a mensagem some da lista.

Teste também os casos de borda:

- Acesse uma URL inexistente, como **http://localhost:8000/mensagens/9999/editar/**.
  Você deve ver a página **404**, e não um erro do servidor — efeito do
  `get_object_or_404`.
- Edite uma mensagem deixando o **título em branco**: o formulário recarrega
  com o erro de validação, sem salvar.

---

A partir de um app que só listava mensagens, você
construiu, passo a passo, todas as quatro operações fundamentais de uma
aplicação web (**C**reate, **R**ead, **U**pdate e **D**elete) direto pela
interface pública, com formulários validados, URLs parametrizadas, proteção
contra CSRF e confirmação antes de apagar.

No caminho, você exercitou os pilares do Django:

- **Models** e relacionamentos (`ForeignKey`, `ManyToManyField`);
- **Migrations** para evoluir o banco;
- **Forms** (`ModelForm`) para validar entrada de dados;
- **Views** que respondem a GET e POST;
- **Templates** reaproveitáveis com a linguagem de templates do Django

