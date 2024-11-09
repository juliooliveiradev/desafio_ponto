# views.py
import logging
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Empresa, Funcionario, Ponto
from .forms import EmpresaForm, FuncionarioForm, PontoForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User

def home(request):
    empresas = Empresa.objects.all()
    funcionarios = Funcionario.objects.all()
    return render(request, 'home.html', {'empresas': empresas, 'funcionarios': funcionarios})

@login_required
def cadastrar_empresa(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        endereco = request.POST.get('endereco')

        if request.user.is_superuser:
            funcionario_id = request.POST.get('funcionario_admin')
            funcionario_admin = Funcionario.objects.get(id=funcionario_id)
            empresa = Empresa.objects.create(nome=nome, endereco=endereco)
            empresa.admin = funcionario_admin  # Define o funcionário admin
            empresa.save()
            messages.success(request, "Empresa cadastrada com admin designado.")
        else:
            Empresa.objects.create(nome=nome, endereco=endereco)
            messages.success(request, "Empresa cadastrada com sucesso.")
        return redirect('home')

    funcionarios = Funcionario.objects.all() if request.user.is_superuser else None
    return render(request, 'cadastrar_empresa.html', {'funcionarios': funcionarios})

# Configurando o logger
logger = logging.getLogger(__name__)

from django.db import IntegrityError, transaction

@login_required
def cadastrar_funcionario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        empresa_id = request.POST.get('empresa')
        senha = request.POST.get('senha')
        
        # Verificação do sobrenome
        nome_split = nome.split(" ")
        if len(nome_split) < 2:
            messages.error(request, "Informe o nome e o sobrenome.")
            return redirect('cadastrar_funcionario')
        
        primeiro_nome = nome_split[0]
        sobrenome = nome_split[1]
        username = f"{primeiro_nome}.{sobrenome}"
        
        # Buscar a empresa
        try:
            empresa = Empresa.objects.get(id=empresa_id)
        except Empresa.DoesNotExist:
            messages.error(request, "Empresa não encontrada.")
            return redirect('cadastrar_funcionario')
        
        # Verificar se o email já está em uso
        if Funcionario.objects.filter(email=email).exists():
            messages.error(request, "Este email já está em uso.")
            return redirect('cadastrar_funcionario')

        try:
            with transaction.atomic():  # Garante que o processo seja tratado como uma transação
                # Criar o usuário associado ao funcionário
                user = User.objects.create_user(username=username, password=senha)
                
                # Verificar se é admin
                if request.user.is_superuser:
                    user.is_staff = 'is_admin' in request.POST  # Define o usuário como staff/admin, se marcado
                
                user.save()
                
                # Criar o funcionário e associá-lo ao usuário
                funcionario = Funcionario.objects.create(
                    nome=nome,
                    email=email,
                    empresa=empresa,
                    user=user  # Associa o usuário criado ao funcionário
                )
                
            messages.success(request, "Funcionário cadastrado com sucesso.")
            return redirect('home')
        
        except IntegrityError as e:
            logger.error(f"IntegrityError: {e}")
            messages.error(request, "Erro ao cadastrar funcionário. Verifique os campos e tente novamente.")
            return redirect('cadastrar_funcionario')

    # Exibir o formulário
    empresas = Empresa.objects.all()
    return render(request, 'cadastrar_funcionario.html', {'empresas': empresas})

@login_required
def registrar_ponto(request):
    funcionario = request.user.funcionario
    hoje = timezone.now().date()

    # Tenta buscar o ponto do dia atual, sem criar automaticamente
    ponto = Ponto.objects.filter(funcionario=funcionario, data=hoje).first()

    if request.method == 'POST':
        # Se não há ponto registrado para o dia, cria um novo
        if ponto is None:
            ponto = Ponto(funcionario=funcionario, data=hoje)
        
        # Registra no primeiro campo vazio encontrado
        if ponto.entrada is None:
            ponto.entrada = timezone.now()
            messages.success(request, "Entrada registrada com sucesso!")
        elif ponto.inicio_intervalo is None:
            ponto.inicio_intervalo = timezone.now()
            messages.success(request, "Início do intervalo registrado com sucesso!")
        elif ponto.fim_intervalo is None:
            ponto.fim_intervalo = timezone.now()
            messages.success(request, "Fim do intervalo registrado com sucesso!")
        elif ponto.saida is None:
            ponto.saida = timezone.now()
            messages.success(request, "Saída registrada com sucesso!")
        else:
            # Exibe a mensagem de erro apenas se todos os campos estiverem preenchidos
            messages.error(request, "Você já registrou todas as batidas para hoje.")
            return redirect('registrar_ponto')

        # Salva o ponto no banco de dados
        ponto.save()
        return redirect('registrar_ponto')

    # Renderiza a página com os campos existentes
    context = {
        'ponto': ponto,
        'hoje': hoje
    }

    return render(request, 'registrar_ponto.html', context)

@login_required
def consultar_ponto(request):
    hoje = timezone.now().date()
    pontos = Ponto.objects.filter(data=hoje)

    if request.user.is_superuser:
        if request.method == 'POST':
            ponto_id = request.POST.get('ponto_id')
            entrada = request.POST.get('entrada')
            inicio_intervalo = request.POST.get('inicio_intervalo')
            fim_intervalo = request.POST.get('fim_intervalo')
            saida = request.POST.get('saida')

            ponto = Ponto.objects.get(id=ponto_id)
            ponto.entrada = entrada
            ponto.inicio_intervalo = inicio_intervalo
            ponto.fim_intervalo = fim_intervalo
            ponto.saida = saida
            ponto.save()
            messages.success(request, "Ponto atualizado com sucesso.")

    return render(request, 'consultar_ponto.html', {'pontos': pontos, 'is_admin': request.user.is_superuser})
