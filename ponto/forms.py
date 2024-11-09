from django import forms
from .models import Empresa, Funcionario, Ponto

class EmpresaForm(forms.ModelForm):

    """
    Formulário para cadastro e edição de empresas.

    Campos:
        nome (str): Nome da empresa.
        endereco (str): Endereço da empresa.
    """

    class Meta:
        model = Empresa
        fields = ['nome', 'endereco']

class FuncionarioForm(forms.ModelForm):

    """
    Formulário para cadastro e edição de funcionários.

    Campos:
        nome (str): Nome do funcionário.
        email (str): Email do funcionário.
        empresa (ForeignKey): Empresa onde o funcionário trabalha.
    """

    class Meta:
        model = Funcionario
        fields = ['nome', 'email', 'empresa']

class PontoForm(forms.ModelForm):

    """
    Formulário para registro de pontos.

    Campos:
        funcionario (ForeignKey): Funcionário associado ao ponto.
        data (DateField): Data do ponto.
        entrada (DateTimeField): Hora de entrada.
        saida (DateTimeField): Hora de saída.
    """

    class Meta:
        model = Ponto
        fields = ['funcionario', 'data', 'entrada', 'inicio_intervalo', 'fim_intervalo', 'saida']
        widgets = {
            'entrada': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'inicio_intervalo': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fim_intervalo': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'saida': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

