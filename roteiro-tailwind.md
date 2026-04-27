# 📘 Página Pessoal — Introdução ao Tailwind CSS

## 🎯 Objetivo

Neste roteiro, você irá aprender como transformar uma página feita com CSS tradicional em uma página utilizando **Tailwind CSS**.

Você aprenderá:

- O que cada classe do Tailwind faz
- Como o Tailwind substitui o CSS tradicional
- Como estilizar diretamente no HTML
- Como identificar padrões de espaçamento, cores e tamanhos


# 🧠 O que é Tailwind CSS?

O **Tailwind CSS** é um framework de estilização.

Diferente do CSS tradicional, em que criamos regras separadas em um arquivo `.css`, o Tailwind permite aplicar estilos diretamente nos elementos HTML usando classes prontas.

### CSS tradicional

```css
.titulo {
  color: blue;
  text-align: center;
}
```

Depois precisamos usar:

```html
<h1 class="titulo">Meu título</h1>
```

---

### Tailwind CSS

```html
<h1 class="text-blue-500 text-center">Meu título</h1>
```

Tudo já é feito diretamente no HTML.

---

# Passo 1 — Inserindo o Tailwind CSS

Antes de usar o Tailwind, precisamos adicioná-lo ao projeto.

Adicione dentro do `<head>`:

```html
<script src="https://cdn.tailwindcss.com"></script>
```

### O que esse código faz?

- `<script>` → adiciona um arquivo JavaScript
- `src="..."` → informa o endereço do Tailwind
- O navegador baixa automaticamente o framework
- Não é necessário instalar nada

### Estrutura mínima do HTML

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Página Pessoal</title>

  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>

</body>
</html>
```


# Passo 2 — Estilizando o BODY

O `body` representa toda a área visível da página.


## CSS original

```css
body {
  background-color: #f5f5f5;
  margin: 40px;
  font-family: Arial;
}
```

## HTML usando Tailwind

```html
<body class="bg-gray-100 font-sans p-10">
```

`bg-gray-100` define a cor de fundo.

- `bg` = background (fundo)
- `gray` = cor cinza
- `100` = intensidade clara

Resultado: 

```css 
background-color: #f3f4f6;
```

`font-sans` define a família da fonte. Equivale a:

```css
font-family: sans-serif;
```


`p-10` adiciona espaçamento interno.

- `p` = padding
- `10` = escala do Tailwind

Equivale aproximadamente a:

```css
padding: 40px;
```


# Passo 3 — Criando um Container

Um container serve para agrupar o conteúdo principal.


## CSS tradicional

```css
.container {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
}
```


## Tailwind

```html
<div class="bg-white p-6 rounded-xl">
```

`bg-white` define fundo branco.

```css
background-color: white;
```

 `p-6` adiciona padding interno.

```css
padding: 24px;
```

`rounded-xl` arredonda os cantos.

```css
border-radius: 12px;
```


## Estrutura completa

```html
<body class="bg-gray-100 font-sans p-10">

  <div class="bg-white p-6 rounded-xl">

  </div>

</body>
```

# Passo 4 — Criando o título

O título principal geralmente usa `<h1>`.

---

## CSS tradicional

```css
.titulo {
  color: #2c3e50;
  text-align: center;
}
```

---

## Tailwind

```html
<h1 class="text-3xl text-center font-bold text-slate-700">
```

---

## Explicando cada comando

### `text-3xl`

Define tamanho da fonte.

Equivale aproximadamente a:

```css
font-size: 30px;
```

---

### `text-center`

Centraliza o texto.

```css
text-align: center;
```

---

### `font-bold`

Deixa a fonte em negrito.

```css
font-weight: bold;
```

---

### `text-slate-700`

Define a cor do texto.

- `slate` = tom de cinza azulado
- `700` = intensidade escura

---

## Código completo

```html
<h1 class="text-3xl text-center font-bold text-slate-700">
  Sobre Mim
</h1>
```

---

# Passo 5 — Inserindo a imagem

A imagem normalmente representa o perfil do aluno.

---

## CSS tradicional

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

---

## Tailwind

```html
<img
  src="foto.jpg"
  class="w-48 rounded-full border-4 border-slate-700 p-1 mx-auto"
>
```

---

## Explicando cada comando

### `w-48`

Define a largura.

```css
width: 192px;
```

---

### `rounded-full`

Transforma a imagem em círculo.

```css
border-radius: 9999px;
```

---

### `border-4`

Adiciona borda.

```css
border-width: 4px;
```

---

### `border-slate-700`

Define a cor da borda.

---

### `p-1`

Adiciona espaço interno.

```css
padding: 4px;
```

---

### `mx-auto`

Centraliza horizontalmente.

- `mx` = margem horizontal
- `auto` = cálculo automático

Equivale a:

```css
margin-left: auto;
margin-right: auto;
```

---

# Passo 6 — Criando subtítulos

Os subtítulos ajudam a separar seções.

---

## CSS tradicional

```css
.subtitulo {
  color: #2c3e50;
}
```

---

## Tailwind

```html
<h2 class="text-2xl font-semibold text-slate-700">
```

---

## Explicando cada comando

### `text-2xl`

Define o tamanho da fonte.

---

### `font-semibold`

Aplica um peso intermediário.

```css
font-weight: 600;
```

---

### `text-slate-700`

Define a cor do texto.

---

# Passo 7 — Criando a lista de interesses

---

## CSS tradicional

```css
.lista {
  background-color: #ecf0f1;
  padding: 15px;
  border-radius: 8px;
}
```

---

## Tailwind

```html
<ul class="bg-slate-100 p-4 rounded-lg">
```

---

## Explicando cada comando

### `bg-slate-100`

Cor de fundo clara.

---

### `p-4`

Adiciona padding.

```css
padding: 16px;
```

---

### `rounded-lg`

Arredonda bordas.

```css
border-radius: 8px;
```

---

# Passo 8 — Criando efeito Hover

Hover é o efeito que acontece quando o mouse passa sobre um elemento.

---

## CSS tradicional

```css
.lista li:hover {
  color: #e74c3c;
}
```

---

## Tailwind

```html
<li class="hover:text-red-500">
```

---

## Explicando cada comando

### `hover:`

Indica um estado especial.

Esse estilo só será aplicado quando o mouse estiver sobre o elemento.

---

### `text-red-500`

Muda a cor do texto.

---

# Passo 9 — Página Completa

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Página Pessoal</title>

  <script src="https://cdn.tailwindcss.com"></script>
</head>

<body class="bg-gray-100 font-sans p-10">

  <div class="bg-white p-6 rounded-xl">

    <h1 class="text-3xl text-center font-bold text-slate-700">
      Sobre Mim
    </h1>

    <img
      src="foto.jpg"
      class="w-48 rounded-full border-4 border-slate-700 p-1 mx-auto"
    >

    <h2 class="text-2xl font-semibold text-slate-700">
      Meus Interesses
    </h2>

    <ul class="bg-slate-100 p-4 rounded-lg">
      <li class="hover:text-red-500">Programação</li>
      <li class="hover:text-red-500">Filmes</li>
      <li class="hover:text-red-500">Jogos</li>
    </ul>

  </div>

</body>
</html>
```

---

# 🎯 Resumo Didático

## CSS tradicional

Exige:

- Criar arquivo CSS
- Criar classes
- Alternar entre HTML e CSS
- Escrever mais código

---

## Tailwind CSS

Permite:

- Estilizar diretamente no HTML
- Desenvolvimento mais rápido
- Menos troca entre arquivos
- Classes reutilizáveis

---

# 🧠 Dica importante

No começo, as classes podem parecer grandes.

Mas com prática, você começa a reconhecer padrões.

Por exemplo:

| Classe | Significado |
|--------|-------------|
| `p-4` | padding |
| `m-4` | margin |
| `text-center` | centralizar texto |
| `rounded-lg` | borda arredondada |
| `bg-blue-500` | fundo azul |
| `font-bold` | negrito |

Com o tempo, você passa a montar layouts rapidamente apenas usando classes.
