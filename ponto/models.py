import datetime
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
import pytz

class Empresa(models.Model):

    """
    Representa uma empresa cadastrada no sistema.

    Atributos:
        nome (str): Nome da empresa.
        endereco (str): Endereço da empresa.
    """

    nome = models.CharField(max_length=100)
    endereco = models.TextField()

    def __str__(self):
        return self.nome
    
class Funcionario(models.Model):

    """
    Representa um funcionário associado a uma empresa.

    Atributos:
        nome (str): Nome do funcionário.
        email (str): Email do funcionário.
        empresa (ForeignKey): A empresa onde o funcionário trabalha.
    """

    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE, related_name="funcionario")

    def __str__(self):
        return self.nome



class Ponto(models.Model):

    """
    Representa um registro de ponto de um funcionário, com horários de 
    entrada, início e fim do intervalo, e saída.

    Atributos:
        funcionario (ForeignKey): Funcionário associado ao ponto.
        data (DateField): Data do ponto.
        entrada (DateTimeField): Hora de entrada.
        inicio_intervalo (DateTimeField): Hora de início do intervalo.
        fim_intervalo (DateTimeField): Hora de fim do intervalo.
        saida (DateTimeField): Hora de saída.
    """

    funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    data = models.DateField()
    entrada = models.DateTimeField(null=True, blank=True)
    inicio_intervalo = models.DateTimeField(null=True, blank=True)
    fim_intervalo = models.DateTimeField(null=True, blank=True)
    saida = models.DateTimeField(null=True, blank=True)

    def batidas_restantes(self):

        """
        Verifica se ainda há horários de ponto pendentes.

        Retorna:
            bool: True se houver batidas pendentes, False caso contrário.
        """

        
        if not self.entrada or not self.inicio_intervalo or not self.fim_intervalo or not self.saida:
            return True 
        return False 

    def registrar_batida(self):
 
        """
        Registra a próxima batida no primeiro campo vazio em sequência.

        As batidas são registradas na sequência: entrada, início do intervalo,
        fim do intervalo, e saída.
        """

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