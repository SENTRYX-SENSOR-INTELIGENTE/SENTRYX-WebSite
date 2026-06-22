# ============================================================
# IMPORTAÇÕES DO PROJETO
# ============================================================
# Aqui importamos as bibliotecas que serão usadas no backend.
#
# Flask:
# Ferramenta principal para criar o servidor web.
#
# render_template:
# Permite abrir/renderizar arquivos HTML pelo Flask.
#
# request:
# Permite receber dados enviados por formulários HTML.
#
# redirect:
# Redireciona o usuário para outra rota/página.
#
# url_for:
# Gera o caminho correto de uma rota Flask.
#
# session:
# Guarda informações do usuário logado enquanto ele navega.
#
# flash:
# Envia mensagens temporárias para aparecerem no HTML.
# Exemplo: "E-mail ou senha incorretos."
#
# PyMySQL:
# Permite conectar o Python ao MySQL local.
#
# psycopg2:
# Permite conectar o Python ao PostgreSQL, usado no Render.
#
# Werkzeug Security:
# Usado para criptografar e validar senhas.
#
# python-dotenv:
# Permite carregar variáveis do arquivo .env localmente.
#
# os:
# Usado para acessar variáveis de ambiente e montar caminhos
# de pastas dentro do projeto.
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, session, flash

import pymysql

# ============================================================
# PostgreSQL / Render
# ============================================================
# psycopg2:
# Biblioteca que permite o Python conversar com PostgreSQL.
# No Render, o banco gratuito usado será PostgreSQL.
#
# psycopg2.extras.RealDictCursor:
# Faz os resultados do PostgreSQL também voltarem como dicionário,
# parecido com o DictCursor do PyMySQL.
# ============================================================

import psycopg2
import psycopg2.extras

from werkzeug.security import generate_password_hash, check_password_hash

# ============================================================
# DOTENV
# ============================================================
# load_dotenv:
# Permite carregar variáveis de ambiente a partir do arquivo .env
# quando estamos rodando o projeto localmente.
#
# Isso evita deixar senha, usuário e chave secreta escritos
# diretamente dentro do código.
# ============================================================

from dotenv import load_dotenv

import os

# Carrega as variáveis do arquivo .env local, se ele existir.
load_dotenv()


# ============================================================
# CONFIGURAÇÃO DE CAMINHO DO PROJETO
# ============================================================
# O arquivo app.py está dentro da pasta:
#
# SENTRYX26/backend/app.py
#
# Mas os arquivos HTML principais estão fora do backend:
#
# SENTRYX26/index.html
# SENTRYX26/indexlogin.html
# SENTRYX26/indexcadastro.html
# SENTRYX26/indexusuario.html
#
# Então precisamos dizer ao Flask:
# "olhe uma pasta acima do backend".
#
# os.path.dirname(__file__):
# Pega a pasta onde o app.py está.
#
# os.path.join(..., '..'):
# Volta uma pasta.
#
# os.path.abspath(...):
# Transforma isso em um caminho completo.
# ============================================================

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


# ============================================================
# CRIAÇÃO DA APLICAÇÃO FLASK
# ============================================================
# app = Flask(...)
# Aqui criamos o servidor Flask.
#
# template_folder=BASE_DIR:
# Diz ao Flask que os arquivos HTML estão na pasta principal
# do projeto SENTRYX26, não dentro de backend/templates.
#
# static_folder=BASE_DIR:
# Diz ao Flask que os arquivos estáticos também estão na pasta
# principal do projeto.
#
# Arquivos estáticos são:
# - css/
# - js/
# - assets/
# - imagens
# - vídeos
#
# static_url_path='':
# Permite que os caminhos antigos continuem funcionando.
#
# Exemplo:
# <link rel="stylesheet" href="css/login.css">
#
# Sem isso, o Flask normalmente procuraria em /static/css/login.css.
# Com essa configuração, ele aceita o caminho css/login.css.
# ============================================================

app = Flask(
    __name__,
    template_folder=BASE_DIR,
    static_folder=BASE_DIR,
    static_url_path=''
)


# ============================================================
# CHAVE SECRETA DO FLASK COM VARIÁVEL DE AMBIENTE
# ============================================================
# A secret_key é usada para proteger sessões e mensagens flash.
#
# Primeiro tentamos buscar a SECRET_KEY no ambiente.
#
# Localmente:
# Ela pode estar no arquivo backend/.env.
#
# No Render:
# Ela será cadastrada em Environment Variables.
#
# Se não encontrar nenhuma SECRET_KEY, usamos um valor padrão
# apenas para desenvolvimento local.
# ============================================================

app.secret_key = os.getenv('SECRET_KEY', 'sentryx_chave_secreta_dev')


# ============================================================
# CONEXÃO COM O BANCO DE DADOS MYSQL
# ============================================================
# Esta função cria uma conexão com o banco sentryx_db.
#
# Sempre que precisarmos consultar ou salvar algo no banco,
# chamamos:
#
# conexao = get_db_connection()
#
# Dados usados:
#
# host='localhost':
# O banco está rodando na sua própria máquina.
#
# user='root':
# Usuário do MySQL.
#
# password='MySQL@2022':
# Senha do seu MySQL.
#
# database='sentryx_db':
# Nome do banco que criamos para a SENTRYX.
#
# port=3307:
# Porta onde seu MySQL está rodando.
#
# cursorclass=pymysql.cursors.DictCursor:
# Faz o resultado das consultas voltar como dicionário.
#
# Exemplo:
# usuario['nome']
# usuario['email']
#
# Fica mais fácil de entender do que usar posição por número.
# ============================================================

def get_db_connection():
    # ========================================================
    # DATABASE_URL - POSTGRESQL NO RENDER
    # ========================================================
    # No Render, o banco PostgreSQL fornece uma variável chamada
    # DATABASE_URL.
    #
    # Essa variável guarda tudo que o sistema precisa para se
    # conectar ao banco online:
    # - usuário;
    # - senha;
    # - host;
    # - porta;
    # - nome do banco.
    #
    # Se DATABASE_URL existir, significa que estamos usando o
    # banco PostgreSQL online do Render.
    # ========================================================

    database_url = os.getenv('DATABASE_URL')

    if database_url:
        return psycopg2.connect(
            database_url,
            cursor_factory=psycopg2.extras.RealDictCursor
        )

    # ========================================================
    # MYSQL LOCAL
    # ========================================================
    # Se DATABASE_URL não existir, usamos o MySQL local.
    #
    # Os dados vêm do arquivo backend/.env.
    #
    # Exemplo de .env local:
    #
    # DB_HOST=localhost
    # DB_USER=root
    # DB_PASSWORD=sua_senha
    # DB_NAME=sentryx_db
    # DB_PORT=3307
    # SECRET_KEY=sua_chave
    # ========================================================

    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME', 'sentryx_db'),
        port=int(os.getenv('DB_PORT', 3307)),
        cursorclass=pymysql.cursors.DictCursor
    )
    
# ============================================================
# ROTA INICIAL DO SITE
# ============================================================
# Esta rota abre a página principal da SENTRYX.
#
# Quando o usuário acessar:
#
# http://127.0.0.1:5000/
#
# O Flask vai renderizar:
#
# index.html
#
# Esse é o fluxo correto:
# O usuário entra no link principal e vê o site institucional.
# ============================================================

@app.route('/')
def index():
    return render_template('index.html')


# ============================================================
# ROTA DE LOGIN
# ============================================================
# Esta rota tem dois comportamentos:
#
# GET:
# Quando o usuário acessa /login pelo navegador.
# Nesse caso, o Flask apenas mostra a tela indexlogin.html.
#
# POST:
# Quando o usuário preenche o formulário e clica em "Entrar".
# Nesse caso, o Flask recebe email e senha, consulta o banco e
# verifica se o login está correto.
#
# No HTML, o formulário está assim:
#
# <form action="/login" method="POST">
#
# Isso significa:
# "envie os dados para a rota /login usando POST".
# ============================================================

@app.route('/login', methods=['GET', 'POST'])
def login():

    # ========================================================
    # Verifica se o formulário foi enviado
    # ========================================================
    # Se request.method for POST, significa que o usuário clicou
    # no botão Entrar do formulário.
    # ========================================================

    if request.method == 'POST':

        # ====================================================
        # RECEBENDO DADOS DO FORMULÁRIO
        # ====================================================
        # O Flask pega os valores dos inputs pelo atributo name.
        #
        # No HTML:
        # <input name="email">
        # <input name="senha">
        #
        # Aqui no Python:
        # request.form.get('email')
        # request.form.get('senha')
        # ====================================================

        email = request.form.get('email')
        senha = request.form.get('senha')

        # ====================================================
        # ABRINDO CONEXÃO COM O BANCO
        # ====================================================
        # Criamos a conexão e o cursor.
        #
        # conexão:
        # É a ligação com o banco.
        #
        # cursor:
        # É o objeto que executa comandos SQL.
        # ====================================================

        conexao = get_db_connection()
        cursor = conexao.cursor()

        # ====================================================
        # BUSCANDO USUÁRIO PELO EMAIL
        # ====================================================
        # Aqui procuramos na tabela usuarios se existe alguém
        # com o email digitado.
        #
        # %s:
        # É um espaço reservado para o valor do email.
        #
        # (email,):
        # É o valor que será colocado no lugar do %s.
        #
        # Fazemos assim para evitar SQL Injection, que é uma
        # falha de segurança comum quando se monta SQL direto
        # com texto do usuário.
        # ====================================================

        cursor.execute(
            "SELECT * FROM usuarios WHERE email = %s",
            (email,)
        )

        # ====================================================
        # PEGANDO O RESULTADO DA CONSULTA
        # ====================================================
        # fetchone() pega apenas um usuário.
        #
        # Se encontrou, usuario recebe os dados.
        # Se não encontrou, usuario recebe None.
        # ====================================================

        usuario = cursor.fetchone()

        # ====================================================
        # FECHANDO CONEXÃO
        # ====================================================
        # Depois da consulta, fechamos o cursor e a conexão.
        # Isso evita deixar conexões abertas sem necessidade.
        # ====================================================

        cursor.close()
        conexao.close()

        # ====================================================
        # VALIDANDO LOGIN
        # ====================================================
        # Primeiro verificamos se o usuário existe.
        #
        # Depois usamos check_password_hash para comparar:
        #
        # - senha criptografada salva no banco
        # - senha digitada no formulário
        #
        # Se estiver correto, criamos a sessão do usuário.
        # ====================================================

        if usuario and check_password_hash(usuario['senha'], senha):

            # =================================================
            # CRIANDO SESSÃO DO USUÁRIO
            # =================================================
            # session guarda dados enquanto o usuário está logado.
            #
            # logged_in:
            # Usamos para saber se o usuário está autenticado.
            #
            # usuario_id:
            # Guardamos o id do usuário para usar futuramente em
            # sensores, contatos, alertas etc.
            #
            # usuario:
            # Guardamos o nome para exibir no dashboard.
            # =================================================

            session['logged_in'] = True
            session['usuario_id'] = usuario['id']
            session['usuario'] = usuario['nome']

            # =================================================
            # REDIRECIONA PARA O DASHBOARD
            # =================================================
            # Se o login deu certo, o usuário vai para a rota:
            #
            # /dashboard
            # =================================================

            return redirect(url_for('dashboard'))

        else:
            # =================================================
            # LOGIN INVÁLIDO
            # =================================================
            # Se o email não existe ou a senha está errada,
            # mostramos uma mensagem na tela usando flash().
            # =================================================

            flash('E-mail ou senha incorretos.')

    # ========================================================
    # ABRIR TELA DE LOGIN
    # ========================================================
    # Se o método for GET, ou se o login der errado,
    # o Flask renderiza novamente a tela indexlogin.html.
    # ========================================================

    return render_template('indexlogin.html')


# ============================================================
# ROTA DE CADASTRO DE USUÁRIO
# ============================================================
# Esta rota também tem dois comportamentos:
#
# GET:
# Abre a tela de cadastro indexcadastro.html.
#
# POST:
# Recebe os dados do formulário, criptografa a senha e salva
# o usuário na tabela usuarios do MySQL.
#
# No HTML, o formulário está assim:
#
# <form action="/cadastro" method="POST">
# ============================================================

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():

    # ========================================================
    # Se for POST, significa que o usuário enviou o formulário.
    # ========================================================

    if request.method == 'POST':

        # ====================================================
        # RECEBENDO DADOS DO FORMULÁRIO DE CADASTRO
        # ====================================================
        # Esses nomes precisam ser iguais aos atributos name
        # do arquivo indexcadastro.html.
        # ====================================================

        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        telefone = request.form.get('telefone')

        # ====================================================
        # CRIPTOGRAFANDO A SENHA
        # ====================================================
        # Nunca salvamos a senha pura no banco.
        #
        # Exemplo ruim:
        # senha = 123456
        #
        # Exemplo correto:
        # senha = scrypt:32768:8:1$...
        #
        # generate_password_hash transforma a senha em um hash.
        # ====================================================

        senha_criptografada = generate_password_hash(senha)

        # ====================================================
        # ABRINDO CONEXÃO COM O BANCO
        # ====================================================

        conexao = get_db_connection()
        cursor = conexao.cursor()

        try:
            # =================================================
            # INSERINDO USUÁRIO NO BANCO
            # =================================================
            # Salvamos nome, email, senha criptografada e telefone
            # na tabela usuarios.
            #
            # A coluna email tem UNIQUE no banco.
            # Isso impede que duas contas usem o mesmo email.
            # =================================================

            cursor.execute(
                """
                INSERT INTO usuarios (nome, email, senha, telefone)
                VALUES (%s, %s, %s, %s)
                """,
                (nome, email, senha_criptografada, telefone)
            )

            # =================================================
            # CONFIRMANDO A GRAVAÇÃO
            # =================================================
            # commit() confirma a operação no banco.
            # Sem commit, o INSERT pode não ser salvo.
            # =================================================

            conexao.commit()

            # =================================================
            # MENSAGEM DE SUCESSO
            # =================================================

            flash('Cadastro realizado com sucesso! Agora faça login.')

            # =================================================
            # REDIRECIONA PARA O LOGIN
            # =================================================
            # Depois de cadastrar, o usuário volta para a tela
            # de login para entrar com a conta criada.
            # =================================================

            return redirect(url_for('login'))

        except pymysql.err.IntegrityError:
            # =================================================
            # ERRO DE EMAIL REPETIDO
            # =================================================
            # Se o email já existir no banco, o MySQL dispara
            # IntegrityError por causa da regra UNIQUE.
            # =================================================

            flash('Este e-mail já está cadastrado.')

        finally:
            # =================================================
            # FECHANDO CONEXÃO
            # =================================================
            # O finally executa sempre, dando certo ou dando erro.
            # Assim garantimos que a conexão será fechada.
            # =================================================

            cursor.close()
            conexao.close()

    # ========================================================
    # ABRIR TELA DE CADASTRO
    # ========================================================
    # Quando o usuário acessa /cadastro pelo navegador,
    # o método é GET, então mostramos indexcadastro.html.
    # ========================================================

    return render_template('indexcadastro.html')


# ============================================================
# ROTA DO DASHBOARD / PAINEL DO USUÁRIO
# ============================================================
# Esta é a área protegida do sistema.
#
# O usuário só pode acessar se estiver logado.
#
# Se tentar acessar /dashboard direto sem login,
# será redirecionado para /login.
# ============================================================

@app.route('/dashboard')
def dashboard():

    # ========================================================
    # PROTEÇÃO DO DASHBOARD
    # ========================================================
    # Se o usuário não estiver logado, ele volta para o login.
    # ========================================================

    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # ========================================================
    # BUSCAR CONTATOS DE EMERGÊNCIA DO USUÁRIO LOGADO
    # ========================================================
    # Pegamos o id do usuário salvo na sessão e buscamos apenas
    # os contatos vinculados a esse usuário.
    #
    # Assim, cada usuário visualiza somente os próprios contatos.
    # ========================================================

    usuario_id = session.get('usuario_id')

    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT id, nome, telefone, parentesco
        FROM contatos_emergencia
        WHERE usuario_id = %s
        ORDER BY id DESC
        """,
        (usuario_id,)
    )

    contatos = cursor.fetchall()

    cursor.close()
    conexao.close()

    # ========================================================
    # ABRIR PAINEL DO USUÁRIO
    # ========================================================
    # Enviamos para o HTML:
    # - nome_usuario: nome do usuário logado
    # - contatos: lista de contatos cadastrados no banco
    # ========================================================

    return render_template(
        'indexusuario.html',
        nome_usuario=session.get('usuario'),
        contatos=contatos
    )
    # ========================================================
    # ABRIR PAINEL DO USUÁRIO
    # ========================================================
    # Se estiver logado, o Flask renderiza a tela existente:
    #
    # indexusuario.html
    # ========================================================

    return render_template(
        'indexusuario.html',
        nome_usuario=session.get('usuario')
    )


# ============================================================
# ROTA DE LOGOUT / SAIR
# ============================================================
# Esta rota limpa a sessão do usuário.
#
# Quando a sessão é limpa, o sistema "esquece" que o usuário
# estava logado.
# ============================================================

@app.route('/logout')
def logout():

    # Limpa todos os dados da sessão.
    session.clear()

    # Depois de sair, volta para a tela de login.
    return redirect(url_for('login'))


# ============================================================
# ROTA DE TESTE DO BANCO
# ============================================================
# Esta rota verifica se o Flask consegue conversar com o banco.
#
# Ela funciona em dois cenários:
#
# 1. MySQL local:
#    Usa SHOW TABLES;
#
# 2. PostgreSQL no Render:
#    Consulta as tabelas pelo information_schema.
#
# Quando acessamos:
#
# http://127.0.0.1:5000/teste-banco
#
# ou, no Render:
#
# https://seu-link.onrender.com/teste-banco
#
# O sistema retorna uma resposta em JSON informando se a conexão
# deu certo e quais tabelas existem.
# ============================================================

@app.route('/teste-banco')
def teste_banco():

    try:
        conexao = get_db_connection()
        cursor = conexao.cursor()

        if os.getenv('DATABASE_URL'):
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public';
            """)
        else:
            cursor.execute("SHOW TABLES;")

        tabelas = cursor.fetchall()

        cursor.close()
        conexao.close()

        return {
            "status": "conectado",
            "mensagem": "Conexão com o banco realizada com sucesso!",
            "tabelas": tabelas
        }

    except Exception as erro:
        return {
            "status": "erro",
            "mensagem": str(erro)
        }
        
        # ============================================================
# ROTA TEMPORÁRIA PARA CRIAR TABELAS NO RENDER
# ============================================================
# Esta rota será usada para criar/verificar as tabelas no banco
# PostgreSQL online do Render.
#
# IMPORTANTE:
# Ela é temporária para facilitar a configuração inicial.
# Depois que o banco estiver criado e funcionando, podemos
# remover essa rota ou proteger com uma chave de segurança.
#
# Para usar no Render:
#
# https://seu-link.onrender.com/criar-tabelas-render
# ============================================================

@app.route('/criar-tabelas-render')
def criar_tabelas_render():
    try:
        conexao = get_db_connection()
        cursor = conexao.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                senha VARCHAR(255) NOT NULL,
                telefone VARCHAR(20),
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensores (
                id SERIAL PRIMARY KEY,
                nome_sensor VARCHAR(100) NOT NULL,
                codigo_sensor VARCHAR(100) UNIQUE NOT NULL,
                local_instalacao VARCHAR(100),
                tipo_gas VARCHAR(50),
                status_sensor VARCHAR(30) DEFAULT 'ativo',
                usuario_id INT NOT NULL,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leituras_gas (
                id SERIAL PRIMARY KEY,
                sensor_id INT NOT NULL,
                nivel_gas DECIMAL(10,2) NOT NULL,
                temperatura DECIMAL(10,2),
                umidade DECIMAL(10,2),
                data_leitura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sensor_id) REFERENCES sensores(id) ON DELETE CASCADE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alertas (
                id SERIAL PRIMARY KEY,
                sensor_id INT NOT NULL,
                nivel_risco VARCHAR(30) NOT NULL,
                mensagem TEXT NOT NULL,
                status_alerta VARCHAR(30) DEFAULT 'pendente',
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sensor_id) REFERENCES sensores(id) ON DELETE CASCADE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contatos_emergencia (
                id SERIAL PRIMARY KEY,
                usuario_id INT NOT NULL,
                nome VARCHAR(100) NOT NULL,
                telefone VARCHAR(20) NOT NULL,
                parentesco VARCHAR(50),
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            );
        """)

        conexao.commit()
        cursor.close()
        conexao.close()

        return {
            "status": "ok",
            "mensagem": "Tabelas criadas/verificadas com sucesso."
        }

    except Exception as erro:
        return {
            "status": "erro",
            "mensagem": str(erro)
        }
        
# ============================================================
# ROTA PARA CADASTRAR CONTATO DE EMERGÊNCIA
# ============================================================
# Esta rota recebe os dados enviados pelo formulário do painel
# do usuário e salva na tabela contatos_emergencia.
#
# O formulário está dentro do indexusuario.html e envia:
# - nome
# - telefone
# - parentesco
#
# A rota usa o usuario_id salvo na sessão para vincular o contato
# ao usuário logado.
# ============================================================

@app.route('/adicionar-contato', methods=['POST'])
def adicionar_contato():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    usuario_id = session['usuario_id']
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    parentesco = request.form.get('parentesco')

    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO contatos_emergencia (usuario_id, nome, telefone, parentesco)
        VALUES (%s, %s, %s, %s)
        """,
        (usuario_id, nome, telefone, parentesco)
    )

    conexao.commit()
    cursor.close()
    conexao.close()

    flash('Contato de emergência cadastrado com sucesso!')
    return redirect(url_for('dashboard'))

# ============================================================
# ROTA PARA EDITAR CONTATO DE EMERGÊNCIA
# ============================================================
# Esta rota recebe os dados alterados no formulário do painel
# e atualiza o contato no banco.
#
# Importante:
# A edição só acontece se o contato pertencer ao usuário logado.
# Isso evita que um usuário edite contato de outro usuário.
# ============================================================

@app.route('/editar-contato/<int:contato_id>', methods=['POST'])
def editar_contato(contato_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    usuario_id = session['usuario_id']
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    parentesco = request.form.get('parentesco')

    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE contatos_emergencia
        SET nome = %s, telefone = %s, parentesco = %s
        WHERE id = %s AND usuario_id = %s
        """,
        (nome, telefone, parentesco, contato_id, usuario_id)
    )

    conexao.commit()
    cursor.close()
    conexao.close()

    flash('Contato de emergência atualizado com sucesso!')
    return redirect(url_for('dashboard'))


# ============================================================
# ROTA PARA EXCLUIR CONTATO DE EMERGÊNCIA
# ============================================================
# Esta rota exclui um contato do banco.
#
# Importante:
# A exclusão só acontece se o contato pertencer ao usuário logado.
# O aviso de confirmação aparece no HTML antes do envio.
# ============================================================

@app.route('/excluir-contato/<int:contato_id>', methods=['POST'])
def excluir_contato(contato_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    usuario_id = session['usuario_id']

    conexao = get_db_connection()
    cursor = conexao.cursor()

    cursor.execute(
        """
        DELETE FROM contatos_emergencia
        WHERE id = %s AND usuario_id = %s
        """,
        (contato_id, usuario_id)
    )

    conexao.commit()
    cursor.close()
    conexao.close()

    flash('Contato de emergência excluído com sucesso!')
    return redirect(url_for('dashboard'))
        
# ============================================================
# INICIAR O SERVIDOR FLASK
# ============================================================
# Este bloco só roda quando executamos diretamente:
#
# python app.py
#
# debug=True:
# Mostra erros detalhados no navegador e reinicia o servidor
# automaticamente quando salvamos alterações.
#
# IMPORTANTE:
# debug=True é bom para desenvolvimento local.
# Em produção/Render, futuramente usamos Gunicorn e debug=False.
# ============================================================

if __name__ == '__main__':
    app.run(debug=True)