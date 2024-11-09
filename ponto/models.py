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




class Ponto(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    data = models.DateField(default=timezone.now)
    entrada = models.DateTimeField(null=True, blank=True, default=timezone.now)
    inicio_intervalo = models.DateTimeField(null=True, blank=True, default=timezone.now)
    fim_intervalo = models.DateTimeField(null=True, blank=True, default=timezone.now)
    saida = models.DateTimeField(null=True, blank=True, default=timezone.now)
    
    def batidas_restantes(self):
        # Retorna True se houver campos não preenchidos
        return not all([self.entrada, self.inicio_intervalo, self.fim_intervalo, self.saida])
    
    def registrar_batida(self):
        # Registra as batidas na sequência
        if not self.entrada:
            self.entrada = timezone.now()
        elif not self.inicio_intervalo:
            self.inicio_intervalo = timezone.now()
        elif not self.fim_intervalo:
            self.fim_intervalo = timezone.now()
        elif not self.saida:
            self.saida = timezone.now()
        self.save()