# Importa a biblioteca 'mysql.connector' para se comunicar com um servidor MySQL
import mysql.connector

# Cria uma conexão com o banco de dados MySQL, utilizando as informações de conexão passadas como parâmetros
conexao = mysql.connector.connect(
    host='localhost',  # Endereço do servidor MySQL
    user='root',  # Nome de usuário do MySQL
    password='SENHA_DO_ROOT',  # Senha do usuário do MySQL
    database='NOME_DO_BD'  # Nome do banco de dados MySQL
)

# Cria um objeto cursor para executar comandos no banco de dados
cursor = conexao.cursor()
