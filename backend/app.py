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
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, session, flash

# ============================================================
# PyMySQL
# ============================================================
# Biblioteca que permite o Python conversar com o banco MySQL.
# Neste projeto, usamos o MySQL local com o banco sentryx_db.
# ============================================================

import pymysql

# ============================================================
# SEGURANÇA DE SENHA
# ============================================================
# generate_password_hash:
# Criptografa a senha antes de salvar no banco.
#
# check_password_hash:
# Compara a senha digitada no login com a senha criptografada
# que está salva no banco.
# ============================================================

from werkzeug.security import generate_password_hash, check_password_hash

# ============================================================
# OS
# ============================================================
# Biblioteca usada para trabalhar com caminhos de pastas.
# Como o app.py está dentro da pasta backend, usamos o os para
# localizar a pasta principal do site SENTRYX26.
# ============================================================

import os


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
# CHAVE SECRETA DO FLASK
# ============================================================
# A secret_key é usada para proteger sessões e mensagens flash.
#
# Sessão:
# Guarda dados do usuário logado.
#
# Flash:
# Mostra mensagens temporárias no HTML.
#
# IMPORTANTE:
# Para um projeto profissional online, essa chave não deve ficar
# escrita diretamente no código. Futuramente, no Render, podemos
# colocar isso em variável de ambiente.
# ============================================================

app.secret_key = 'sentryx_chave_secreta'


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
    return pymysql.connect(
        host='localhost',
        user='root',
        password='MySQL@2022',
        database='sentryx_db',
        port=3307,
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
    # Verifica se existe logged_in na sessão.
    #
    # Se não existir, significa que o usuário não fez login.
    # ========================================================

    if not session.get('logged_in'):
        return redirect(url_for('login'))

    # ========================================================
    # ABRIR PAINEL DO USUÁRIO
    # ========================================================
    # Se estiver logado, o Flask renderiza a tela existente:
    #
    # indexusuario.html
    # ========================================================

    return render_template('indexusuario.html')


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
# Esta rota foi criada para verificar se o Flask consegue
# conversar com o banco MySQL sentryx_db.
#
# Quando acessamos:
#
# http://127.0.0.1:5000/teste-banco
#
# O Flask tenta executar:
#
# SHOW TABLES;
#
# Se der certo, retorna status conectado e a lista de tabelas.
# ============================================================

@app.route('/teste-banco')
def teste_banco():

    try:
        # Abre conexão com o banco.
        conexao = get_db_connection()
        cursor = conexao.cursor()

        # Executa comando SQL para listar as tabelas do banco.
        cursor.execute("SHOW TABLES;")

        # Pega todas as tabelas retornadas.
        tabelas = cursor.fetchall()

        # Fecha conexão.
        cursor.close()
        conexao.close()

        # Retorna uma resposta em formato de dicionário.
        # O Flask transforma isso em JSON no navegador.
        return {
            "status": "conectado",
            "mensagem": "Conexão com o banco sentryx_db realizada com sucesso!",
            "tabelas": tabelas
        }

    except Exception as erro:
        # Se algo der errado, mostramos o erro.
        # Isso ajuda a identificar problemas de conexão, senha,
        # porta, nome do banco etc.
        return {
            "status": "erro",
            "mensagem": str(erro)
        }


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