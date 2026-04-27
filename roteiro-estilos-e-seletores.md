# 📘 Roteiro — Seletores e Estilos

## 🎯 Objetivo
Nesta atividade, você vai:

- Aprender como adicionar estilos em HTML
- Entender como funciona o CSS
- Criar uma página pessoal estilizada
- Aprender a usar seletores CSS
- Evoluir o código passo a passo
- Separar HTML e CSS gradualmente


# Passo 0 - O que é CSS?

CSS significa **Cascading Style Sheets**.

Ele é responsável pela aparência visual da página.

Com CSS podemos:

- Alterar cores
- Ajustar tamanhos
- Posicionar elementos
- Criar bordas
- Trabalhar com espaçamento
- Melhorar o visual do site


## Adicionando CSS diretamente nos elementos

O CSS pode ser escrito diretamente dentro das tags HTML.

Isso é chamado de **CSS inline**.

Exemplo:

```html
<h1 style="color: blue; text-align: center;">Sobre mim</h1>
```

### Explicando:

- `style=""` → adiciona CSS diretamente ao elemento
- `color: blue` → muda a cor do texto
- `text-align: center` → centraliza o conteúdo

Outro exemplo:

```html
<body style="background-color: #f5f5f5; margin: 40px; font-family: Arial;">
```

### Explicando:

- `background-color` → muda a cor de fundo
- `margin` → adiciona espaço nas bordas
- `font-family` → define a fonte

### Exemplo completo usando CSS inline

```html
<body style="background-color: #f5f5f5; margin: 40px; font-family: Arial;">

  <h1 style="color: #2c3e50; text-align: center;">Sobre mim</h1>

  <img src="https://github.com/USERNAME.png"
       style="width: 200px; border-radius: 50%; display: block; margin: auto;">

  <p style="text-align: center; font-weight: bold;">Meu nome é [SEU NOME] </p>

</body>
```


## Problema do CSS inline

Apesar de funcionar, o CSS inline possui algumas limitações:

- O código fica repetitivo
- Fica difícil de organizar
- A manutenção se torna complicada
- Não reaproveita estilos

Por isso, geralmente usamos CSS dentro da tag `<style>`.


# Passo 1 — Movendo CSS para a tag Style

Agora vamos organizar o código da página pessoal, que foi criada no roteiro anterior.

Em vez de colocar CSS em cada elemento, colocamos tudo dentro da tag:

```html
<style>

</style>
```

Essa tag fica dentro do `<head>`.

```html
<head>
  <meta charset="UTF-8">
  <title>Sobre mim</title>

  <style>

  </style>
</head>
```

---

# Passo 2 — Estilizando o Body

O seletor `body` representa toda a página.

```css
body {
  background-color: #f5f5f5;
  margin: 40px;
  font-family: Arial;
}
```

### Explicando:

- `background-color` → cor de fundo
- `margin` → espaço externo da página
- `font-family` → tipo de fonte

### Resultado esperado

A página terá:

- Fundo cinza claro
- Espaçamento nas bordas
- Fonte Arial

4. **COMMIT & PUSH**.


---

# Passo 3 — Criando uma área central

1. Agora vamos organizar o conteúdo dentro de uma caixa.

HTML:

```html
<div class="container">

</div>
```

Coloque todo o conteúdo dentro dessa `<div>`.

CSS:

```css
.container {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
}
```

### Explicando:

- `.container` → seletor de classe
- `background-color` → fundo branco
- `padding` → espaço interno
- `border-radius` → cantos arredondados


**COMMIT & PUSH**.


---

# 📌 Entendendo seletores CSS

Existem vários tipos de seletores.

---

## 1️Seletor por tag

Seleciona diretamente uma tag HTML.

```css
body {

}
```

Aplica estilo para todo o `<body>`.

---

## Seletor por classe

Usa ponto (`.`).

```css
.container {

}
```

HTML:

```html
<div class="container">
```

Permite reutilizar estilos.

---

## Seletor por ID

Usa cerquilha (`#`).

```css
#nome {

}
```

HTML:

```html
<p id="nome">Meu nome é Aline</p>
```

O ID normalmente deve ser único.

---

# Passo 4 — Estilizando o título

HTML:

```html
<h1 class="titulo">Sobre mim</h1>
```

CSS:

```css
.titulo {
  color: #2c3e50;
  text-align: center;
}
```

**COMMIT & PUSH**.


### Explicando:

- `color` → cor do texto
- `text-align` → alinhamento

---

# Passo 5 — Estilizando a imagem

HTML:

```html
<img class="foto" src="https://avatars.githubusercontent.com/u/14023536?v=4">
```

CSS:

```css
.foto {
  width: 200px;
  border-radius: 50%;
  border: 3px solid #2c3e50;
  padding: 5px;
  display: block;
  margin: auto;
}
```

**COMMIT & PUSH**.


### Explicando:

- `width` → largura da imagem
- `border-radius: 50%` → deixa redonda
- `border` → adiciona borda
- `padding` → espaço interno
- `display: block` → permite centralizar
- `margin: auto` → centraliza horizontalmente

---

# Passo 6 — Estilizando o nome

HTML:

```html
<p id="nome">Meu nome é Aline</p>
```

CSS:

```css
#nome {
  text-align: center;
  font-weight: bold;
}
```

**COMMIT & PUSH**.


### Explicando:

- `text-align` → centraliza o texto
- `font-weight` → deixa em negrito

---

# Passo 7 — Estilizando subtítulos

HTML:

```html
<h2 class="subtitulo">Meus interesses</h2>
```

CSS:

```css
.subtitulo {
  color: #2c3e50;
}
```

**COMMIT & PUSH**.


---

# Passo 8 — Estilizando listas

HTML:

```html
<ul class="lista">
  <li>Programação</li>
  <li>Filmes</li>
  <li>Jogos</li>
</ul>
```

CSS:

```css
.lista {
  background-color: #ecf0f1;
  padding: 15px;
  border-radius: 8px;
}
```

**COMMIT & PUSH**.


### Explicando:

- `background-color` → fundo da lista
- `padding` → espaço interno
- `border-radius` → bordas arredondadas

---

# Passo 9 — Estilizando elementos internos

Podemos selecionar elementos dentro de outros.

CSS:

```css
.lista li {
  margin-bottom: 10px;
}
```

**COMMIT & PUSH**.


Isso significa:

- Selecionar todos os `<li>` que estão dentro da classe `.lista`

---

# Passo 10 — Criando efeito Hover

Hover acontece quando passamos o mouse.

CSS:

```css
.lista li:hover {
  color: #e74c3c;
}
```

**COMMIT & PUSH**.


### Explicando:

- `:hover` → ativa quando o mouse passa sobre o elemento


# Passo 11 — Separando CSS em outro arquivo

Depois que o CSS crescer, é melhor separar.

Crie um arquivo chamado:

```text
style.css
```

Remova o conteúdo de dentro do `<style>`.

No HTML, adicione:

```html
<link rel="stylesheet" href="style.css">
```

Dentro do `<head>`:

```html
<head>
  <meta charset="UTF-8">
  <title>Sobre mim</title>
  <link rel="stylesheet" href="style.css">
</head>
```
