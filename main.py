# Importa as bibliotecas necessárias para o bot Discord e MySQL
import discord
import mysql.connector
from discord.ext import commands
from discord import app_commands

# Importa as variáveis 'cursor' e 'conexao' da biblioteca 'cnx'
from cnx import cursor, conexao

# Atribui o ID do servidor do Discord a uma variável
id_do_servidor = 00 #ID_DO_SERVIDOR


# Define a classe 'Client', que herda da classe 'discord.Client'
class client(discord.Client):
    def log(self, command_name, user_name):
        print(f"\nComando '{command_name}' executado por '{user_name}'")

    # Define o método construtor '__init__', que é executado ao criar uma instância da classe 'Client'
    def __init__(self):

        # Chama o método construtor da classe pai 'discord.Client' e passa as intenções padrão como parâmetro
        super().__init__(intents=discord.Intents.default())

        # Atribui um valor booleano 'False' à variável 'synced'
        self.synced = False

        # Atribui o valor 1080490737159901205 à variável 'channel_id'
        self.channel_id = 00 #ID_DO_CANAL_PRIVADO

        # Cria um objeto 'CommandTree' e passa a instância da classe 'Client' como parâmetro
        tree = app_commands.CommandTree(self)



#Copiar a partir DAQUI!!!!!!!!

        # Define um comando para o bot chamado 'verificar_integridade', que verifica a integridade do bot e do banco de dados
        @tree.command(guild=discord.Object(id=id_do_servidor), name='verificar_integridade', description='Verifica a integridade do bot e do banco de dados.')
        async def verificar_integridade(interaction: discord.Interaction):
            if interaction.channel_id != self.channel_id:  # Verifica o canal
                await interaction.response.send_message(content="Canal errado rapaz! kkkkk", ephemeral=True)
                return
            else:
                try:
                    cursor.execute("SELECT COUNT(*) FROM usuarios")
                    num_usuarios = cursor.fetchone()[0]
                    resposta = f"O bot está funcionando corretamente e há {num_usuarios} usuários cadastrados no banco de dados."
                    await interaction.response.send_message(content=resposta, ephemeral=True)
                    
                except Exception as e:
                    await interaction.response.send_message(content=f"Ocorreu um erro ao verificar a integridade do bot e do banco de dados: {e}", ephemeral=True)
            user_name = interaction.user.name
            self.log('verificar_integridade', user_name)



        # Define um comando para o bot chamado 'cargo', que adiciona um usuário ao banco de dados
        @tree.command(guild=discord.Object(id=id_do_servidor), name='cargo', description='Adiciona usuário ao banco de dados.')
        async def cargo(interaction: discord.Interaction, nome: str, cargo: str):
            if interaction.channel_id != self.channel_id:  # Verifica o canal
                await interaction.response.send_message(f"```fix\nCanal errado rapais! kkkkk\n```", ephemeral=True)
                return
            else:
                try:
                    zero = 0
                    # Cria uma query SQL para inserir o usuário no banco de dados com os dados fornecidos
                    cursor = conexao.cursor() # Abrindo o cursor para executar uma consulta no banco de dados
                    inserir_usuario = f'INSERT INTO usuarios (user, cargo, traducao, revisao, clrd, typer, qc, saldo) VALUES ("{nome}","{cargo}", {zero}, {zero}, {zero}, {zero}, {zero}, {zero})'
                    # Executa a query SQL no cursor e faz commit na conexão
                    cursor.execute(inserir_usuario)
                    conexao.commit() # Salvando as alterações no banco de dados
                    cursor.close() # Fechando o cursor para liberar recursos do sistema
                    # Envia uma mensagem de sucesso com a menção do usuário que executou o comando, nome do usuário e o cargo adicionado
                    resposta = f"{interaction.user.mention}, o usuário {nome} com o cargo {cargo} foi adicionado ao banco de dados."
                    await interaction.response.send_message(f"diff\n+ {resposta}\n", ephemeral=True)
                except Exception as e:
                    # Se ocorrer um erro durante a execução do comando, uma mensagem de erro será enviada ao usuário
                    await interaction.response.send_message(f"```diff\n- Ocorreu um erro ao adicionar o usuário ao banco de dados: {e}\n```", ephemeral=True)
                # Registra a ação no log
                user_name = interaction.user.name
                self.log('cargo', user_name)




            
        # Definindo a função atualizar_trabalho() para atualizar o valor de um trabalho feito pelo usuário na tabela "usuarios"
        def atualizar_trabalho(nome, trabalho, valor):
            cursor = conexao.cursor() # Abrindo o cursor para executar uma consulta no banco de dados
            sql = f"UPDATE usuarios SET {trabalho} = {trabalho} + {valor} WHERE user = '{nome}'" # Construindo a consulta SQL para atualizar o valor correspondente na tabela "usuarios"
            cursor.execute(sql) # Executando a consulta SQL
            conexao.commit() # Salvando as alterações no banco de dados
            cursor.close() # Fechando o cursor para liberar recursos do sistema

        # Definindo a função app_command() para ouvir o comando "job"
        @tree.command(guild=discord.Object(id=id_do_servidor), name='job', description='Registra o trabalho feito pelo usuário.')
        async def job(interaction: discord.Interaction, nome: str, trabalho: str, valor: str):
                if interaction.channel_id != self.channel_id:  # Verifica o canal
                    await interaction.response.send_message(f"```fix\nCanal errado rapais! kkkkk\n```", ephemeral=True)
                    return
                else:
                    # Verificando se o trabalho escolhido é válido
                    trabalhos_validos = ["traducao", "revisao", "clear", "cldr", "typesetter", "qc"]
                    if trabalho not in trabalhos_validos: # Se o trabalho escolhido não estiver na lista de trabalhos válidos, envia uma mensagem de erro e sai da função
                        await interaction.response.send_message(f"{nome}, trabalho inválido. Por favor, escolha um dos seguintes trabalhos: {', '.join(trabalhos_validos)}.", ephemeral=True)
                        return

                    # Pesquisando o nome do usuário na tabela "usuarios"
                    cursor = conexao.cursor() # Abrindo o cursor para executar uma consulta no banco de dados
                    sql = f"SELECT * FROM usuarios WHERE user = '{nome}'" # Construindo a consulta SQL para buscar um usuário na tabela "usuarios" pelo nome
                    cursor.execute(sql) # Executando a consulta SQL
                    resultado = cursor.fetchone() # Obtendo o primeiro registro retornado pela consulta SQL
                    cursor.close() # Fechando o cursor para liberar recursos do sistema

                    # Se o usuário não estiver na tabela, adicioná-lo com todos os trabalhos com 0
                    if resultado is None: # Se não houver nenhum registro retornado pela consulta SQL, significa que o usuário não está na tabela "usuarios"
                        cursor = conexao.cursor() # Abrindo o cursor para executar uma consulta no banco de dados
                        sql = f"INSERT INTO usuarios (user, cargo, traducao, revisao, clear, cldr, typesetter, qc) VALUES ('{nome}', '', 0, 0, 0, 0, 0, 0)" # Construindo a consulta SQL para inserir um novo registro na tabela "usuarios" com todos os trabalhos com valor 0
                        cursor.execute(sql) # Executando a consulta SQL
                        conexao.commit() # Salvando as alterações no banco de dados
                        cursor.close() # Fechando o cursor para liberar recursos do sistema
                        resultado = (nome, '', 0, 0, 0, 0, 0, 0) # Definindo o valor de resultado como uma tupla com o nome do usuário, o cargo vazio e todos os trabalhos com valor 0

                    # Atualizando o valor correspondente na tabela "usuarios"
                    atualizar_trabalho(nome, trabalho, valor)

                    # Enviando a mensagem de confirmação
                    await interaction.response.send_message(f"{nome}, trabalho de {trabalho} adicionado para {nome}.", ephemeral=True)
                    
                user_name = interaction.user.name
                self.log('job', user_name)
                

                   
        @tree.command(guild=discord.Object(id=id_do_servidor), name='userjob', description='Mostrar dados de trabalho de um User.')
        async def userjob(interaction: discord.Interaction, nome: str):
            cursor = conexao.cursor()
            sql = f"SELECT cargo, traducao, revisao, clrd, typer, qc FROM usuarios WHERE user = '{nome}'"
            cursor.execute(sql)
            resultado = cursor.fetchone()
            cursor.close()

            if resultado is None:
                await interaction.response.send_message(f"{nome} não foi encontrado na lista de usuários.", ephemeral=True)
                return
                    
            # Obtendo os valores de cada tipo de trabalho usando os nomes de coluna
            cargo, traducao, revisao, clrd, typer, qc = resultado
                
            saldo = traducao * 1.25 + revisao + clrd * 1.5 + typer * 2 + qc
                
            # Atualizando o valor da coluna para zero
            cursor = conexao.cursor()
            sql = f"UPDATE usuarios SET saldo = {saldo} WHERE user = '{nome}'"
            cursor.execute(sql)
            conexao.commit()
            cursor.close() 

            # Formatando a mensagem de resposta usando f-strings
            resposta1 = f'\n   {nome}'
            resposta = f'```Capítulos feitos no mês:\n'
            resposta += f'Tradução: {traducao:02d}\n'
            resposta += f'Revisão: {revisao:02d}\n'
            resposta += f'Edição: {clrd:02d}\n'
            resposta += f'Typer: {typer:02d}\n'
            resposta += f'QC: {qc:02d}\n'
            resposta += f'Saldo: {saldo:.2f}```'


            # Usando as constantes predefinidas do objeto Embed
            embed = discord.Embed(description=f"{resposta1}\n{resposta}", color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
                
            user_name = interaction.user.name
            self.log('userjob', user_name)



        @tree.command(guild=discord.Object(id=id_do_servidor), name='resetjob', description='Reseta o trabalho feito pelo usuário.')
        async def resetjob(interaction: discord.Interaction, nome: str):
            if interaction.channel_id != self.channel_id:  # Verifica o canal
                await interaction.response.send_message(f"```fix\nCanal errado rapais! kkkkk\n```", ephemeral=True)
                return

            # Pesquisando o nome do usuário na tabela "usuarios"
            cursor = conexao.cursor()
            sql = "SELECT * FROM usuarios WHERE user = %s"
            cursor.execute(sql, (nome,))
            resultado = cursor.fetchone()
            cursor.close()

            if resultado is None:
                # Se o usuário não estiver na tabela, adicioná-lo com todos os trabalhos com 0
                cursor = conexao.cursor()
                sql = "INSERT INTO usuarios (user, cargo, traducao, revisao, clrd, typer, qc) VALUES (%s, '', 0, 0, 0, 0, 0, 0)"
                cursor.execute(sql, (nome,))
                conexao.commit()
                cursor.close()
                resultado = (nome, '', 0, 0, 0, 0, 0, 0)

            # Atualiza todos os trabalhos para zero
            cursor = conexao.cursor()
            sql = f"UPDATE usuarios SET traducao = 0, revisao = 0, clrd = 0, typer = 0, qc = 0 WHERE user = %s"
            cursor.execute(sql, (nome,))
            conexao.commit()
            cursor.close()

            # Enviando a mensagem de confirmação
            await interaction.response.send_message(f"{nome}, todos os trabalhos registrados foram resetados para 0.", ephemeral=True)

            user_name = interaction.user.name
            self.log('resetjob', user_name)
    


        
        # Define um comando para o bot chamado 'dados_do_banco', que mostra todos os dados do banco de dados
        @tree.command(guild=discord.Object(id=id_do_servidor), name='dados_do_banco', description='Mostra todos os dados do banco de dados.')
        async def dados_do_banco(interaction: discord.Interaction):
            # Verifica se o comando foi enviado no canal correto
            if interaction.channel_id != self.channel_id:
                await interaction.response.send_message(content="Canal errado rapaz! kkkkk", ephemeral=True)
                return
            else:
                try:
                    # Executa uma consulta SQL para selecionar todos os dados do banco de dados
                    cursor.execute("SELECT * FROM usuarios")
                    # Recupera todos os resultados da consulta
                    dados = cursor.fetchall()
                    # Monta uma resposta com todos os dados recuperados do banco de dados
                    resposta = "Dados do banco de dados:\n"
                    for dado in dados:
                        saldo = dado[8]
                        resposta += f"\nUsuário: {dado[1]}\n"
                    # Envia a resposta com todos os dados do banco de dados de volta para o usuário que solicitou
                    await interaction.response.send_message(content=resposta, ephemeral=True)


                except Exception as e:
                    # Envia uma mensagem de erro caso ocorra uma exceção ao tentar recuperar os dados do banco de dados
                    await interaction.response.send_message(content=f"Ocorreu um erro ao mostrar os dados do banco de dados: {e}", ephemeral=True)
                
                # Registra a ação na log do bot
                user_name = interaction.user.name
                self.log('dados_do_banco', user_name)
                
        # Comando para excluir um usuário da tabela 'usuarios'
        @tree.command(guild=discord.Object(id=id_do_servidor), name='excluir_usuario', description='Exclui um usuário do banco de dados.')
        async def excluir_usuario(interaction: discord.Interaction, nome: str):
            if interaction.channel_id != self.channel_id:  # Verifica o canal
                await interaction.response.send_message(f"```fix\nCanal errado rapais! kkkkk\n```", ephemeral=True)
                return
            else:
                try:
                    # Cria uma query SQL para excluir o usuário da tabela com o nome fornecido
                    excluir_usuario = f'DELETE FROM usuarios WHERE user = "{nome}"'
                    # Executa a query SQL no cursor e faz commit na conexão
                    cursor.execute(excluir_usuario)
                    conexao.commit()
                    # Envia uma mensagem de sucesso com a menção do usuário que executou o comando e o nome do usuário excluído
                    resposta = f"{interaction.user.mention}, o usuário {nome} foi excluído do banco de dados."
                    await interaction.response.send_message(f"diff\n+ {resposta}\n", ephemeral=True)
                except Exception as e:
                    # Se ocorrer um erro durante a execução do comando, uma mensagem de erro será enviada ao usuário
                    await interaction.response.send_message(f"```diff\n- Ocorreu um erro ao excluir o usuário do banco de dados: {e}\n```", ephemeral=True)
                user_name = interaction.user.name
                self.log('excluir_usuario', user_name)

        self.tree = tree
        
#Até aqui copiar



    async def on_ready(self):
        await self.tree.sync(guild=discord.Object(id=id_do_servidor))
        self.synced = True
        print(f"Entremos como {self.user}.")

aclient = client()
aclient.run('TOKEN_DO_BOT')