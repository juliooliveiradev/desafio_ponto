import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
import pytz

class Empresa(models.Model):
    nome = models.CharField(max_length=100)
    endereco = models.TextField()

    def __str__(self):
        return self.nome
    
class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE, related_name="funcionario")

    def __str__(self):
        return self.nome



class Ponto(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    data = models.DateField()
    entrada = models.DateTimeField(null=True, blank=True)
    inicio_intervalo = models.DateTimeField(null=True, blank=True)
    fim_intervalo = models.DateTimeField(null=True, blank=True)
    saida = models.DateTimeField(null=True, blank=True)

    def batidas_restantes(self):
        # Verifica se há algum campo de batida que ainda não foi preenchido
        if not self.entrada or not self.inicio_intervalo or not self.fim_intervalo or not self.saida:
            return True  # Existem batidas restantes para registrar
        return False  # Todos os campos de batida estão preenchidos

    def registrar_batida(self):
        # Registra a batida no primeiro campo vazio
        if self.entrada is None:
            self.entrada = timezone.now()
        elif self.inicio_intervalo is None:
            self.inicio_intervalo = timezone.now()
        elif self.fim_intervalo is None:
            self.fim_intervalo = timezone.now()
        elif self.saida is None:
            self.saida = timezone.now()

        self.save()


    
    def __str__(self):
        return f"{self.funcionario.nome} - {self.data}"