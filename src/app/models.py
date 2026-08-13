from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.contrib.auth.hashers import identify_hasher
from django.core.validators import MinValueValidator, MaxValueValidator
from multi_email_field.fields import MultiEmailField

# Create your models here.

STATUS = [
    ("andamento", "Em Andamento"),
    ("finalizado", "Finalizado"),
    ("abandonado", "Abandonado"),
]

FASE = [
    ("web", "Web"),
    ("distribuido", "Distribuído"),
    ("corporativo", "Corporativo"),
]

PLATAFORMA = [
    ("web", "Web"),
    ("mobile", "Mobile"),
    ("vr", "VR"),
    ("desktop", "Desktop"),
    ("console", "Console"),
]


class Usuario(AbstractUser):
    """
    Modelo customizado de usuário.
    Estende o AbstractUser do Django para adicionar campos específicos do ReTecer.
    """

    # Campos adicionais podem ser adicionados conforme necessidade

    nome = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    # senha, gerenciado pelo Django
    matricula = models.CharField(max_length=14, blank=True, null=True)

    username = None  # Remove o campo username padrão do AbstractUser
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = "usuarios"
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        try:
            identify_hasher(self.password)
        except Exception:
            self.set_password(self.password)
        super().save(*args, **kwargs)


class Orientador(Usuario):

    class Meta:
        db_table = "orientadores"
        verbose_name = "Orientador"
        verbose_name_plural = "Orientadores"

    def __str__(self):
        return self.email


class Orientando(Usuario):

    class Meta:
        db_table = "orientandos"
        verbose_name = "Orientando"
        verbose_name_plural = "Orientandos"

    def __str__(self):
        return self.email


class Tecnologia(models.Model):

    nome = models.CharField(max_length=255)
    icone = models.ImageField(upload_to="tecnologias/")

    class Meta:
        db_table = "tecnologias"
        verbose_name = "Tecnologia"
        verbose_name_plural = "Tecnologias"

    def __str__(self):
        return self.nome


class Categoria(models.Model):

    nome = models.CharField(max_length=255)

    class Meta:
        db_table = "categorias"
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome


class Projeto(models.Model):

    titulo = models.CharField(max_length=255)
    descricao = models.TextField(max_length=500)
    avaliacao = models.FloatField(default=0.0, blank=True, null=True)

    data_criacao = models.DateTimeField()
    data_finalizacao = models.DateTimeField(blank=True, null=True)
    data_publicacao = models.DateTimeField()

    categoria_principal = models.ForeignKey(
        Categoria, on_delete=models.CASCADE, related_name="projetos_principais"
    )
    categorias_secundarias = models.ManyToManyField(
        Categoria,
        related_name="projetos_secundarios",
        blank=True,
    )

    projetos_favoritos = models.ManyToManyField(
        Usuario,
        related_name="favoritos",
        blank=True,
    )

    status = models.CharField(max_length=20, choices=STATUS, default="andamento")
    fase = models.CharField(max_length=20, choices=FASE)
    plataforma = models.CharField(max_length=20, choices=PLATAFORMA)
    tecnologias = models.ManyToManyField(
        Tecnologia, related_name="projetos", blank=True
    )

    resumo = models.TextField(max_length=2000)
    imagem = models.ImageField(upload_to="projetos/")
    repositorio = models.URLField(max_length=500)
    contato = MultiEmailField(max_length=500, blank=True, null=True)
    ano_semestre = models.CharField(max_length=20)
    colaboradores = models.TextField()
    contatos = MultiEmailField(max_length=500, blank=True, null=True)
    orientador = models.CharField(max_length=255)

    class Meta:
        db_table = "projetos"
        verbose_name = "Projeto"
        verbose_name_plural = "Projetos"

    def __str__(self):
        return self.titulo


class Avaliar(models.Model):

    nota = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )  # máx 5. min 1
    comentario = models.TextField(max_length=255, blank=True, null=True)

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)

    class Meta:
        db_table = "avaliacoes"
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "projeto"], name="unique_avaliacao"
            )
        ]

    def __str__(self):
        return f"{self.usuario.email} avaliou {self.projeto.titulo} com {self.nota}"


# OrientandoProjeto
class Participacao(models.Model):

    orientando = models.ForeignKey(Orientando, on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    participacao = models.BooleanField()

    class Meta:
        db_table = "participacoes"
        verbose_name = "Participação"
        verbose_name_plural = "Participações"

    def __str__(self):
        return f"{self.orientando.nome} participa de {self.projeto.titulo}"


class OrientadorProjeto(models.Model):

    orientador = models.ForeignKey(Orientador, on_delete=models.CASCADE)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    participacao = models.BooleanField()

    class Meta:
        db_table = "orientadorprojeto"
        verbose_name = "Orientadores do Projeto"
        verbose_name_plural = "Orientadores dos Projetos"

    def __str__(self):
        return f"{self.orientador.nome} participa de {self.projeto.titulo}"
