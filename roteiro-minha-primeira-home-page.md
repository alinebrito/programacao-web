# 📘 Roteiro — Minha primeira página pessoal

## 🎯 Objetivo
Nesta atividade, você vai:
- Criar e hospedar um site utilizando o GitHub Pages
- Criar a primeira versão da sua página pessoal


# Passo 0 — Criando conta (se necessário)

Acesse e crie uma conta, se necessário : https://github.com


# Passo 1 — Código inicial

Clicar em *New Repository*

Nomear como: username.github.io (Esse nome é especial, ativa automaticamente o GitHub Pages). Exemplo: ``maria.github.io``

Marcar:
* Public
* Add README


# Passo 2 — Criando a primeira página

1. Adicione um arquivo de nome `index.html`
3. Inserir o código básico:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Minha Primeira Página</title>
</head>
<body>
    <h1>Olá, mundo!</h1>
    <p>Meu nome é [SEU NOME]</p>
    <p>Este é meu primeiro site 🎉</p>
</body>
</html>
```
4. **COMMIT & PUSH**.


# Passo 3 — Publicando no GitHub Pages

1. Ir em Settings
2. Clicar em Pages
3. Em *Branch*, selecionar: `main` e salvar. Após alguns segundos/minutos, aparecerá o link parecido com: https://username.github.io

---

# Passo 4 — Melhorando a página

Modifique o conteúdo da página, completando com as suas informações abaixo:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Sobre mim</title>
</head> 
<body>
    <h1>Sobre mim</h1>

    <p>Meu nome é ...</p>

    <h2>Meus interesses</h2>
    <ul>
        <li>Programação</li>
        <li>Filmes</li>
        <li>Jogos</li>
    </ul>
</body>
```

Explicando cada parte:
* `<!DOCTYPE html>`→ Informa ao navegador que o documento utiliza HTML5.
* `<html lang="pt-br">` → Define que o idioma principal da página é português do Brasil.
* `<head>`→ Área reservada para configurações da página.
* `<meta charset="UTF-8">` → Permite exibir corretamente caracteres especiais e acentos.
* `<title>` → Define o nome exibido na aba do navegador.
* `<body> → Contém todo o conteúdo visível da página.

4. **COMMIT & PUSH**.


# Passo 5 — Adicionando foto de perfil

1. No GitHub, a foto de perfil segue um padrão de URL. Basta substituir USERNAME pelo usuário. Vamos utilizar essa imagem para melhorar a página: https://github.com/USERNAME.png


2. Modifique o código, conforme exemplo abaixo. Observe que:

* <img> mostra uma imagem
* src = endereço da imagem
* width = tamanho
* border-radius: 50% = deixa redonda

```html

<body>
    <h1>Sobre mim</h1>

    <img src="https://github.com/USERNAME.png" 
         alt="Foto de perfil" 
         width="200" 
         style="border-radius: 50%;">

    <p>Meu nome é ...</p>

    <h2>Meus interesses</h2>
    <ul>
        <li>Programação</li>
        <li>Filmes</li>
        <li>Jogos</li>
    </ul>
</body>

```

4. **COMMIT & PUSH**.



# Passo 6 — Executando o site localmente

Antes de publicar, você pode testar sua página no seu próprio computador.

1.Abra o terminal (ou prompt de comando)

2. Navegue até a pasta onde está o arquivo `index.html`. Exemplo: `cd caminho/da/sua/pasta`

3. Execute o comando:  `python -m http.server`

4. Abra o navegador e acesse: http://localhost:8000

O que isso faz?
* Cria um servidor web local
* Permite visualizar sua página como se estivesse na internet
*   Atualizações no arquivo aparecem ao recarregar a página (F5)