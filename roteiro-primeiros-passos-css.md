# 📘 Roteiro — Primeiros passos com CSS

## 🎯 Objetivo
Nesta atividade, você vai:
- Entender como o CSS altera uma página
- Modificar estilos passo a passo
- Ver o resultado em tempo real

---

## 💻 Editor que vamos usar
Acesse o editor online:

https://www.w3schools.com/css/tryit.asp?filename=trycss_intro

---

# Passo 0 — Código inicial

Copie e cole no editor e clique em **Run**:

```html
<!DOCTYPE html>
<html>
<head>
<style>
body {
  font-family: Arial;
}

h1 {
  color: black;
}

p {
  font-size: 16px;
}

button {
  padding: 5px;
}
</style>
</head>

<body>

<h1>Minha primeira página</h1>
<p>Esse é um parágrafo de exemplo.</p>

<button>Clique aqui</button>

</body>
</html>
```

---

# Passo 1 — Mudando a cor do título

Altere apenas a cor do título:

```html
h1 {
  color: blue;
}
```

Pergunta: O que mudou?

---

# Passo 2 — Cor de fundo

Adicione ao body:

```css
background-color: #e6f0ff;
```

Pergunta: Como o fundo muda a percepção?

---

# Passo 3 — Tamanho do texto

```css
p {
  font-size: 20px;
}
```

Pergunta: Melhorou a leitura?

---

# Passo 4 — Criando uma caixa

Envolva o conteúdo com:

```html
<div class="container">
  ...
</div>
```

E adicione:

```css
.container {
  background-color: white;
}
```

---

# Passo 5 — Centralizando

```css
.container {
  width: 300px;
  margin: 50px auto;
}
```

Pergunta: O que significa “auto”?

---

# Passo 6 — Espaçamento

```css
padding: 20px;
```

Pergunta: Qual a diferença entre margin e padding?

---

# Passo 7 — Ajustando cores

```css
h1 {
  color: #3366cc;
}
```

---

# Passo 8 — Botão

```css
button {
  background-color: #3366cc;
  color: white;
  padding: 10px;
  border: none;
}
```

---

# Passo 9 — Bordas arredondadas

```css
.container {
  border-radius: 10px;
}

button {
  border-radius: 8px;
}
```

Teste valores diferentes!

---

# Desafio — Encontre o erro

```css
body {
  background-color: white;
  color: white;
}

h1 {
  color: blu;
}
```

Perguntas:
- Por que o texto sumiu?
- Onde está o erro?

---

# Desafio final

- Escolha outras cores
- Ajuste tamanhos
- Melhore o visual

---

# Conclusão

Com poucas propriedades CSS, você já consegue criar páginas mais bonitas e organizadas.

