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