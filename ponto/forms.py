from django import forms
from .models import Empresa, Funcionario, Ponto

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nome', 'endereco']

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'email', 'empresa']

class PontoForm(forms.ModelForm):
    class Meta:
        model = Ponto
        fields = ['funcionario', 'data', 'entrada', 'saida']
