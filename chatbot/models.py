from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Curso(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Aluno(models.Model):
    matricula = models.CharField(max_length=100, unique=True)
    nome = models.CharField(max_length=100)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    disciplinas = models.ManyToManyField(Disciplina)

    def __str__(self):
        return f"{self.nome} ({self.matricula})"

class UsuarioSessao(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=20)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)  # Alterado para ForeignKey
    disciplinas = models.ManyToManyField(Disciplina)
    inicio_sessao = models.DateTimeField(auto_now_add=True)

    def tempo_restante(self):
        duracao = timezone.now() - self.inicio_sessao
        tempo_maximo = timezone.timedelta(minutes=15)
        return max(tempo_maximo - duracao, timezone.timedelta())

    def __str__(self):
        return f"Sessão de {self.user.username}"
