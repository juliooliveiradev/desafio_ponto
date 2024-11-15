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

    """
    Exibe a página inicial com uma lista de todas as empresas e funcionários.

    Args:
        request: Objeto HTTP contendo metadados da requisição.

    Returns:
        Renderiza a página 'home.html' com os dados de empresas e funcionários.
    """

    empresas = Empresa.objects.all()
    funcionarios = Funcionario.objects.all()
    return render(request, 'home.html', {'empresas': empresas, 'funcionarios': funcionarios})

@login_required
def cadastrar_empresa(request):

    """
    Exibe o formulário de cadastro de empresa e permite que o usuário cadastrado (superusuário) 
    ou funcionário comum cadastre uma nova empresa. O superusuário pode designar um administrador.

    Args:
        request: Objeto HTTP contendo metadados da requisição.

    Returns:
        Redireciona para a página inicial após o cadastro da empresa com sucesso,
        ou exibe o formulário de cadastro em caso de requisição GET.
    """

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

    """
    Exibe o formulário de cadastro de funcionário e permite que o usuário cadastre um novo funcionário. 
    O superusuário pode designar o funcionário como administrador.

    Args:
        request: Objeto HTTP contendo metadados da requisição.

    Returns:
        Redireciona para a página inicial após o cadastro com sucesso, 
        ou exibe o formulário com uma mensagem de erro em caso de falha.
    """

    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        empresa_id = request.POST.get('empresa')
        senha = request.POST.get('senha')
        
        
        nome_split = nome.split(" ")
        if len(nome_split) < 2:
            messages.error(request, "Informe o nome e o sobrenome.")
            return redirect('cadastrar_funcionario')
        
        primeiro_nome = nome_split[0]
        sobrenome = nome_split[1]
        username = f"{primeiro_nome}.{sobrenome}"
        
        
        try:
            empresa = Empresa.objects.get(id=empresa_id)
        except Empresa.DoesNotExist:
            messages.error(request, "Empresa não encontrada.")
            return redirect('cadastrar_funcionario')
        
        
        if Funcionario.objects.filter(email=email).exists():
            messages.error(request, "Este email já está em uso.")
            return redirect('cadastrar_funcionario')

        try:
            with transaction.atomic():  
                
                user = User.objects.create_user(username=username, password=senha)
                
                
                if request.user.is_superuser:
                    user.is_staff = 'is_admin' in request.POST  # Define o usuário como staff/admin, se marcado
                
                user.save()
                
                
                funcionario = Funcionario.objects.create(
                    nome=nome,
                    email=email,
                    empresa=empresa,
                    user=user  
                )
                
            messages.success(request, "Funcionário cadastrado com sucesso.")
            return redirect('home')
        
        except IntegrityError as e:
            logger.error(f"IntegrityError: {e}")
            messages.error(request, "Erro ao cadastrar funcionário. Verifique os campos e tente novamente.")
            return redirect('cadastrar_funcionario')

    
    empresas = Empresa.objects.all()
    return render(request, 'cadastrar_funcionario.html', {'empresas': empresas})

@login_required
def registrar_ponto(request):
    funcionario = request.user.funcionario
    hoje = timezone.now().date()

    
    ponto = Ponto.objects.filter(funcionario=funcionario, data=hoje).first()

    if request.method == 'POST':
        if ponto is None:
            ponto = Ponto(funcionario=funcionario, data=hoje)
        
        
        if ponto.batidas_restantes():
            ponto.registrar_batida()
            messages.success(request, "Ponto registrado com sucesso!")
        else:
            messages.error(request, "Você já registrou todas as batidas para hoje.")
        
        ponto.save()
        return redirect('registrar_ponto')

    
    context = {
        'ponto': ponto,
        'hoje': hoje
    }

    return render(request, 'registrar_ponto.html', context)

@login_required
def consultar_ponto(request):

    """
    Exibe a página de consulta de pontos registrados com filtro por mês e ano. 
    Permite a edição dos pontos para administradores.

    Args:
        request: Objeto HTTP contendo metadados da requisição.

    Returns:
        Renderiza a página de consulta de ponto ('consultar_ponto.html') com os pontos 
        registrados, opções de filtro de data e funcionalidade de edição para admin.
    """

    hoje = timezone.now().date()
    mes_atual = hoje.month
    ano_atual = hoje.year

    
    mes = request.GET.get('mes', mes_atual)
    ano = request.GET.get('ano', ano_atual)

    funcionario = request.user.funcionario
    pontos = Ponto.objects.filter(funcionario=funcionario, data__month=mes, data__year=ano)

    is_admin = request.user.is_staff

    if request.method == 'POST' and is_admin:
        for key, value in request.POST.items():
            if key.startswith('ponto_'):
                try:
                    ponto_id, campo = key.split('_')[1], key.split('_')[2]
                    ponto = Ponto.objects.get(id=ponto_id)

                    if campo in ['entrada', 'inicio_intervalo', 'fim_intervalo', 'saida']:
                        try:
                            datetime_value = timezone.make_aware(timezone.datetime.strptime(value, '%Y-%m-%dT%H:%M'))
                            setattr(ponto, campo, datetime_value)
                            ponto.save()
                        except ValueError:
                            continue

                except (Ponto.DoesNotExist, ValueError):
                    continue

        messages.success(request, "Pontos atualizados com sucesso!")
        return redirect('consultar_ponto')

    meses = [(i, f'{i:02d}') for i in range(1, 13)]
    anos = [ano_atual, ano_atual - 1, ano_atual + 1]

    context = {
        'pontos': pontos,
        'meses': meses,
        'anos': anos,
        'mes_selecionado': mes,
        'ano_selecionado': ano,
        'is_admin': is_admin
    }
    return render(request, 'consultar_ponto.html', context)
