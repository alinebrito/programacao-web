# Roteiro — Construindo um site com Django + Tailwind + Docker

Esta é a continuação do roteiro para você construir, do zero, o projeto
`demo-django`: um site simples de uma página, escrito em **Django**, estilizado
com **Tailwind CSS** (via CDN), salvando dados em **SQLite** e executado dentro
de um container **Docker**.

Nesta roteiro, você terá uma página inicial que lista mensagens cadastradas no banco
através do painel administrativo do Django.

---

## Sumário


16. [Criar o usuário admin e cadastrar mensagens](#16-criar-o-usuário-admin-e-cadastrar-mensagens)
17. [Para experimentar em aula](#17-para-experimentar-em-aula)

---

### 1. Executar e parar o projeto

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

---

## 2. Criar o usuário admin e cadastrar mensagens

Com o servidor rodando, **abra um segundo terminal** na mesma pasta e execute:

```bash
docker compose exec web python manage.py createsuperuser
```

Informe um nome de usuário, e-mail (opcional) e senha. Em seguida:

1. Acesse **http://localhost:8000/admin/**.
2. Faça login com o usuário criado.
3. Clique em **Mensagens → Adicionar**.
4. Preencha título e conteúdo e salve.
5. Volte a **http://localhost:8000/** — sua mensagem aparece na lista.

Executando esse passo e o roteiro anterior, você acabou de construir um site completo com modelo, view,
template, banco de dados e admin.

Agora, você pode acessar o painel de administração.

Acesse o menu Admin no DJango (menu superior), utilizando as credenciais de acesso que você cadastrou:

http://localhost:8000/admin/


## Cadastrando uma mensagem

Após realizar o login no painel administrativo, acesse: `Home --> Mensagens`

Em seguida, cadastre uma nova mensagem, conforme o exemplo abaixo:

<img src="imagens/turorial-django-mensagem-teste.png" alt="Tutorial Django Parte 1" width="600">

Depois, retorne à página principal e observe que a nova mensagem cadastrada será exibida.

Por fim, abra o código correspondente no Django e tente compreender como ocorre o processo de cadastro e exibição da mensagem.

## 2. Adicionar um campo no model

Exemplo:

 `autor = models.CharField(max_length=80)`)

 
  ```bash
  docker compose run --rm web python manage.py makemigrations
  docker compose run --rm web python manage.py migrate
  ```
  Depois mostre o novo campo no template (`{{ m.autor }}`).

3. Mudar o visual da página:

Edite as classes Tailwind em `templates/home/index.html`.

Troque `from-slate-900 via-indigo-900` por outro gradiente, por exemplo.

# 3. Criar uma nova página** 

Exemplo: `/sobre/`:

  1. Adicione uma função em `home/views.py`:
     ```python
     def sobre(request):
         return render(request, "home/sobre.html")
     ```
  2. Adicione a rota em `home/urls.py`:
     ```python
     path("sobre/", views.sobre, name="sobre"),
     ```
  3. Crie `templates/home/sobre.html`.

# 4. Filtrar mensagens** na view: troque `Mensagem.objects.all()` por
  `Mensagem.objects.filter(titulo__icontains="oi")` e veja só as que contêm "oi"
  no título.

---

## Fluxo MTV (Model–Template–View)

Resumo do que acontece quando alguém acessa `http://localhost:8000/`:

```
Navegador
   ↓
core/urls.py        →  encaminha "/" para o app home
   ↓
home/urls.py        →  encaminha "" para a view index
   ↓
home/views.py       →  consulta o banco via models.py
   ↓
home/models.py      →  ORM converte para SQL no SQLite
   ↓
templates/home/index.html  →  renderiza o HTML com os dados
   ↓
HTML pronto         →  navegador exibe a página
```

Esse é o **padrão MTV** do Django (equivalente ao MVC clássico):

- **Model** = `home/models.py` (estrutura dos dados).
- **Template** = `templates/home/index.html` (apresentação).
- **View** = `home/views.py` (lógica que junta dados + template).

---

## Estrutura final do projeto

```
demo-django/
├── core/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── home/
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/
│   └── home/
│       └── index.html
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── README.md
└── requirements.txt
```
