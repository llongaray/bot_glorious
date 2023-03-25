# Importa a biblioteca 'mysql.connector' para se comunicar com um servidor MySQL
import mysql.connector

# Cria uma conexão com o banco de dados MySQL, utilizando as informações de conexão passadas como parâmetros
conexao = mysql.connector.connect(
    host='localhost',  # Endereço do servidor MySQL
    user='bot',  # Nome de usuário do MySQL
    password='K4mzkhiwMk',  # Senha do usuário do MySQL
    database='bot_glorious'  # Nome do banco de dados MySQL
)

# Cria um objeto cursor para executar comandos no banco de dados
cursor = conexao.cursor()
