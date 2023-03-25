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
                        inserir_usuario = f'INSERT INTO usuarios (user, cargo, traducao, revisao, clear, cldr, typesetter, qc, saldo) VALUES ("{nome}","{cargo}", {zero}, {zero}, {zero}, {zero}, {zero}, {zero}, {zero})'
                        # Executa a query SQL no cursor e faz commit na conexão
                        cursor.execute(inserir_usuario)
                        conexao.commit()
                        # Envia uma mensagem de sucesso com a menção do usuário que executou o comando, nome do usuário e o cargo adicionado
                        resposta = f"{interaction.user.mention}, o usuário {nome} com o cargo {cargo} foi adicionado ao banco de dados."
                        await interaction.response.send_message(f"diff\n+ {resposta}\n", ephemeral=True)
                    except Exception as e:
                        # Se ocorrer um erro durante a execução do comando, uma mensagem de erro será enviada ao usuário
                        await interaction.response.send_message(f"```diff\n- Ocorreu um erro ao adicionar o usuário ao banco de dados: {e}\n```", ephemeral=True)
                    user_name = interaction.user.name
                    self.log('cargo', user_name)


            
        # Definindo a função atualizar_trabalho() para atualizar o valor de um trabalho feito pelo usuário na tabela "usuarios"
        def atualizar_trabalho(nome, trabalho):
            cursor = conexao.cursor() # Abrindo o cursor para executar uma consulta no banco de dados
            sql = f"UPDATE usuarios SET {trabalho} = {trabalho} + 1 WHERE user = '{nome}'" # Construindo a consulta SQL para atualizar o valor correspondente na tabela "usuarios"
            cursor.execute(sql) # Executando a consulta SQL
            conexao.commit() # Salvando as alterações no banco de dados
            cursor.close() # Fechando o cursor para liberar recursos do sistema

        # Definindo a função app_command() para ouvir o comando "job"
        @tree.command(guild=discord.Object(id=id_do_servidor), name='job', description='Registra o trabalho feito pelo usuário.')
        async def job(interaction: discord.Interaction, nome: str, trabalho: str):
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
                    atualizar_trabalho(nome, trabalho)

                    # Enviando a mensagem de confirmação
                    await interaction.response.send_message(f"{nome}, trabalho de {trabalho} adicionado para {nome}.", ephemeral=True)
                    
                user_name = interaction.user.name
                self.log('job', user_name)

        @tree.command(guild=discord.Object(id=id_do_servidor), name='userjob', description='Mostrar dados de trabalho de um User.')
        async def userjob(interaction: discord.Interaction, nome: str):
            if interaction.channel_id != self.channel_id:
                await interaction.response.send_message(f"```fix\nCanal errado rapais! kkkkk\n```", ephemeral=True)
                return

            try:
                cursor = conexao.cursor()
                sql = f"SELECT cargo, traducao, revisao, clear, cldr, typesetter, qc FROM usuarios WHERE user = '{nome}'"
                cursor.execute(sql)
                resultado = cursor.fetchone()
                cursor.close()

                if resultado is None:
                    await interaction.response.send_message(f"{nome} não foi encontrado na lista de usuários.", ephemeral=True)
                    return

                # Obtendo os valores de cada tipo de trabalho usando os nomes de coluna
                cargo, traducao, revisao, clear, cldr, typesetter, qc = resultado

                # Formatando a mensagem de resposta usando f-strings
                resposta1 = f'\n   {nome}'
                resposta = f'```Capítulos feitos no mês:\n'
                resposta += f'Tradução: {traducao:02d}\n'
                resposta += f'Revisão: {revisao:02d}\n'
                resposta += f'Clear: {clear:02d}\n'
                resposta += f'CLRD: {cldr:02d}\n'
                resposta += f'Typesetter: {typesetter:02d}\n'
                resposta += f'QC: {qc:02d}```'

                # Usando as constantes predefinidas do objeto Embed
                embed = discord.Embed(description=f"{resposta1}\n{resposta}", color=discord.Color.purple())
                await interaction.response.send_message(embed=embed, ephemeral=True)

            except Exception as e:
                # Lidando com exceções
                await interaction.response.send_message(f"Ocorreu um erro: {e}", ephemeral=True)
                
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
                sql = "INSERT INTO usuarios (user, cargo, traducao, revisao, clear, cldr, typesetter, qc) VALUES (%s, '', 0, 0, 0, 0, 0, 0)"
                cursor.execute(sql, (nome,))
                conexao.commit()
                cursor.close()
                resultado = (nome, '', 0, 0, 0, 0, 0, 0)

            # Atualiza todos os trabalhos para zero
            cursor = conexao.cursor()
            sql = f"UPDATE usuarios SET traducao = 0, revisao = 0, clear = 0, cldr = 0, typesetter = 0, qc = 0 WHERE user = %s"
            cursor.execute(sql, (nome,))
            conexao.commit()
            cursor.close()

            # Enviando a mensagem de confirmação
            await interaction.response.send_message(f"{nome}, todos os trabalhos registrados foram resetados para 0.", ephemeral=True)

            user_name = interaction.user.name
            self.log('resetjob', user_name)
    

        # Definindo a função app_command() para ouvir o comando "saldo"
        @tree.command(guild=discord.Object(id=id_do_servidor), name='saldo', description='Exibe o saldo do usuário.')
        async def saldo(interaction: discord.Interaction, nome: str):
                if interaction.channel_id != self.channel_id:  # Verifica o canal
                    await interaction.response.send_message(f"```fix\nCanal errado rapais! kkkkk\n```", ephemeral=True)
                    return
                else:
                    # Selecionando o usuário na tabela "usuarios"
                    cursor = conexao.cursor()
                    sql = f"SELECT * FROM usuarios WHERE user = '{nome}'"
                    cursor.execute(sql)
                    resultado = cursor.fetchone()
                    cursor.close()
                    
                    saldo = resultado[3]*1.25
                    print(f'Saldo 3: {saldo}')
                    saldo += resultado[4]
                    print(f'Saldo 4: {saldo}')
                    saldo += (resultado[5]+resultado[6])*1.5
                    print(f'Saldo 5 com 6: {saldo}')
                    saldo += resultado[7]*2
                    print(f'Saldo 7: {saldo}')

                    # Atualizando o valor da coluna para zero
                    cursor = conexao.cursor()
                    sql = f"UPDATE usuarios SET saldo = {saldo} WHERE user = '{nome}'"
                    cursor.execute(sql)
                    conexao.commit()
                    cursor.close()            
                    
                    # Exibindo o saldo do usuário
                    # await interaction.response.send_message(f"💸Saldo {nome}:💸\n```R$: {saldo}\n```")

                    # Enviando a mensagem de resposta
                    cor = 0x800080
                    embed = discord.Embed(description=f"💸 Saldo {nome}:\n```R$: {saldo}\n```", color=cor, ephemeral=True)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    
                user_name = interaction.user.name
                self.log('saldo', user_name)
        
        
        self.tree = tree

    async def on_ready(self):
        await self.tree.sync(guild=discord.Object(id=id_do_servidor))
        self.synced = True
        print(f"Entremos como {self.user}.")

aclient = client()
aclient.run('TOKEN_DO_BOT')