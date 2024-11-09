# Projeto Django - Ponto Eletrônico

Este projeto é uma aplicação Django para o gerenciamento de ponto eletrônico de funcionários, permitindo o registro de entradas, intervalos e saídas, bem como a consulta e edição dos pontos registrados. Além disso, a aplicação possibilita o cadastro de empresas e funcionários, com controle de acessos para administradores.

## Funcionalidades

- **Página Inicial**: Exibe todas as empresas e funcionários.
- **Cadastro de Empresa**: Permite cadastrar uma nova empresa e designar um funcionário administrador.
- **Cadastro de Funcionário**: Permite cadastrar novos funcionários associados a empresas.
- **Registro de Ponto**: Registra as batidas de ponto (Entrada, Início Intervalo, Fim Intervalo, Saída).
- **Consulta de Ponto**: Permite consultar e editar registros de ponto para um mês e ano selecionados.

## Requisitos

- Python 3.x
- Django 3.x ou superior
- Banco de dados PostgreSQL (ou outro de sua preferência, configurável)
- Virtualenv ou venv para ambiente isolado

## Configuração do Ambiente

### 1. Clonar o repositório

Primeiramente, clone o repositório para o seu ambiente local:

```bash
git clone https://github.com/seu-usuario/ponto-eletronico.git
cd ponto-eletronico
```

### 2. Criar um ambiente virtual
### Crie um ambiente virtual para isolar as dependências do projeto:
```
bash
python3 -m venv venv
````
# Ative o ambiente virtual:

No Windows:
bash
````
venv\Scripts\activate
````
No macOS/Linux:
````
bash
source venv/bin/activate
````
### 3. Instalar as dependências
Instale as dependências necessárias usando o pip:
````
bash
pip install -r requirements.txt
````
### 4. Configurar o banco de dados
Certifique-se de que você tenha um banco de dados configurado no seu ambiente. Caso esteja usando o PostgreSQL, edite o arquivo settings.py para ajustar as configurações de conexão do banco de dados:
````
python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nome_do_banco',
        'USER': 'usuario',
        'PASSWORD': 'senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
````
### 5. Realizar as migrações
Execute as migrações para criar as tabelas no banco de dados:
````
bash
python manage.py migrate
````
### 6. Criar um superusuário (administrador)
Para acessar a área administrativa e gerenciar o sistema, crie um superusuário com o seguinte comando:
````
bash
python manage.py createsuperuser
````
Siga as instruções para definir o nome de usuário, e-mail e senha do superusuário.

### 7. Rodar o servidor de desenvolvimento
Após configurar o banco de dados e o superusuário, inicie o servidor de desenvolvimento:
````
bash
python manage.py runserver
````
O servidor estará disponível em http://localhost:8000.

### Estrutura do Projeto
home.html: Página inicial do sistema, onde são exibidos funcionários e empresas.
cadastrar_empresa.html: Formulário para cadastro de empresas.
cadastrar_funcionario.html: Formulário para cadastro de funcionários.
registrar_ponto.html: Formulário para registrar pontos (entrada, intervalos e saída).
consultar_ponto.html: Página para consulta e edição de pontos de funcionários.

## Como Contribuir
Faça o fork deste repositório.
Crie uma branch para a sua feature (git checkout -b minha-feature).
Realize suas modificações.
Faça o commit das suas alterações (git commit -am 'Adiciona nova feature').
Envie para o repositório remoto (git push origin minha-feature).
Abra um Pull Request.

### Licença
Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para mais detalhes.


