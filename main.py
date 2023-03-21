import discord
import mysql.connector
from discord.ext import commands
from discord import app_commands
from cnx import cursor, conexao

id_do_servidor = 1078354743665115186

class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

        tree = app_commands.CommandTree(self)

        @tree.command(guild=discord.Object(id=id_do_servidor), name='verificar_integridade', description='Verifica a integridade do bot e do banco de dados.')
        async def verificar_integridade(interaction: discord.Interaction):
            try:
                cursor.execute("SELECT COUNT(*) FROM usuarios")
                num_usuarios = cursor.fetchone()[0]
                resposta = f"O bot está funcionando corretamente e há {num_usuarios} usuários cadastrados no banco de dados."
                await interaction.response.send_message(f"```fix\n{resposta}\n```", ephemeral=False)
            except Exception as e:
                await interaction.response.send_message(f"```diff\n- Ocorreu um erro ao verificar a integridade do bot e do banco de dados: {e}\n```", ephemeral=False)

        @tree.command(guild=discord.Object(id=id_do_servidor), name='cargo', description='Adiciona usuário ao banco de dados.')
        async def cargo(interaction: discord.Interaction, nome: str, cargo: str):
            try:
                zero = 0
                inserir_usuario = f'INSERT INTO usuarios (user, cargo, traducao, revisao, clear, cldr, typesetter, qc) VALUES ("{nome}","{cargo}", {zero}, {zero}, {zero}, {zero}, {zero}, {zero})'
                cursor.execute(inserir_usuario)
                conexao.commit()
                resposta = f"{interaction.user.mention}, o usuário {nome} com o cargo {cargo} foi adicionado ao banco de dados."
                await interaction.response.send_message(f"diff\n+ {resposta}\n", ephemeral=False)
            except Exception as e:
                await interaction.response.send_message(f"```diff\n- Ocorreu um erro ao adicionar o usuário ao banco de dados: {e}\n```", ephemeral=False)

                # Função para atualizar o trabalho na tabela "usuarios"
        def atualizar_trabalho(nome, trabalho):
            cursor = conexao.cursor()
            sql = f"UPDATE usuarios SET {trabalho} = {trabalho} + 1 WHERE user = '{nome}'"
            cursor.execute(sql)
            conexao.commit()
            cursor.close()

        # Definindo a função app_command() para ouvir o comando "job"
        @tree.command(guild=discord.Object(id=id_do_servidor), name='job', description='Registra o trabalho feito pelo usuário.')
        async def job(interaction: discord.Interaction, nome: str, trabalho: str):
            
            # Verificando se o trabalho escolhido é válido
            trabalhos_validos = ["traducao", "revisao", "clear", "cldr", "typesetter", "qc"]
            if trabalho not in trabalhos_validos:
                await interaction.response.send_message(f"{nome}, trabalho inválido. Por favor, escolha um dos seguintes trabalhos: {', '.join(trabalhos_validos)}.")
                return

            # Pesquisando o nome do usuário na tabela "usuarios"
            cursor = conexao.cursor()
            sql = f"SELECT * FROM usuarios WHERE user = '{nome}'"
            cursor.execute(sql)
            resultado = cursor.fetchone()
            cursor.close()

            # Se o usuário não estiver na tabela, adicioná-lo com todos os trabalhos com 0
            if resultado is None:
                cursor = conexao.cursor()
                sql = f"INSERT INTO usuarios (user, cargo, traducao, revisao, clear, cldr, typesetter, qc) VALUES ('{nome}', '', 0, 0, 0, 0, 0, 0)"
                cursor.execute(sql)
                conexao.commit()
                cursor.close()
                resultado = (nome, '', 0, 0, 0, 0, 0, 0)

            # Atualizando o valor correspondente na tabela "usuarios"
            atualizar_trabalho(nome, trabalho)

            # Enviando a mensagem de confirmação
            await interaction.response.send_message(f"{nome}, trabalho de {trabalho} adicionado para {nome}.")

        @tree.command(guild=discord.Object(id=id_do_servidor), name='userjob', description='Mostrar dados de trabalho de um User.')
        async def userjob(interaction: discord.Interaction, nome: str):

            # Selecionando o usuário na tabela "usuarios"
            cursor = conexao.cursor()
            sql = f"SELECT * FROM usuarios WHERE user = '{nome}'"
            cursor.execute(sql)
            resultado = cursor.fetchone()
            cursor.close()

            # Se o usuário não estiver na tabela, enviar uma mensagem de erro
            if resultado is None:
                await interaction.response.send_message(f"{nome} não foi encontrado na lista de usuários.")
                return

            # Obtendo os valores de cada tipo de trabalho
            cargo = resultado[2]
            traducao = resultado[3]
            revisao = resultado[4]
            clear = resultado[5]
            cldr = resultado[6]
            typesetter = resultado[7]
            qc = resultado[8]

            # Formatação das cores
            cor = 0x800080
            cor_verde = 0x00FF00

            # Formatando a mensagem de resposta
            resposta1 = f'\n   {nome}'
            resposta = f'```Capítulos feitos no mês:\nTradução: {traducao:02d}\n'
            resposta += f'Revisão: {revisao:02d}\n'
            resposta += f'Clear: {clear:02d}\n'
            resposta += f'CLRD: {cldr:02d}\n'
            resposta += f'Typpesetter: {typesetter:02d}\n'
            resposta += f'QC: {qc:02d}```'
            
            # Enviando a mensagem de resposta
            embed = discord.Embed(description=f"{resposta1}\n{resposta}", color=cor)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        # Definindo a função app_command() para ouvir o comando "resetjob"
        @tree.command(guild=discord.Object(id=id_do_servidor), name='resetjob', description='Reseta o trabalho feito pelo usuário.')
        async def resetjob(interaction: discord.Interaction, nome: str, trabalho: str):

            # Verificando se o trabalho escolhido é válido
            trabalhos_validos = ["traducao", "revisao", "clear", "cldr", "typesetter", "qc"]
            if trabalho not in trabalhos_validos:
                await interaction.response.send_message(f"{nome}, trabalho inválido. Por favor, escolha um dos seguintes trabalhos: {', '.join(trabalhos_validos)}.")
                return

            # Pesquisando o nome do usuário na tabela "usuarios"
            cursor = conexao.cursor()
            sql = f"SELECT * FROM usuarios WHERE user = '{nome}'"
            cursor.execute(sql)
            resultado = cursor.fetchone()
            cursor.close()

            # Se o usuário não estiver na tabela, adicioná-lo com todos os trabalhos com 0
            if resultado is None:
                cursor = conexao.cursor()
                sql = f"INSERT INTO usuarios (user, cargo, traducao, revisao, clear, cldr, typesetter, qc) VALUES ('{nome}', '', 0, 0, 0, 0, 0, 0)"
                cursor.execute(sql)
                conexao.commit()
                cursor.close()
                resultado = (nome, '', 0, 0, 0, 0, 0, 0)

            # Verificando se o valor da coluna correspondente ao trabalho escolhido é diferente de zero
            index = trabalhos_validos.index(trabalho) + 3  # Índice da coluna na tupla resultado
            if resultado[index] != 0:
                # Atualizando o valor da coluna para zero
                cursor = conexao.cursor()
                sql = f"UPDATE usuarios SET {trabalho} = 0 WHERE user = '{nome}'"
                cursor.execute(sql)
                conexao.commit()
                cursor.close()

                # Enviando a mensagem de confirmação
                await interaction.response.send_message(f"{nome}, os trabalhos registrados foram resetados para 0.")

        # Definindo a função app_command() para ouvir o comando "saldo"
        @tree.command(guild=discord.Object(id=id_do_servidor), name='saldo', description='Exibe o saldo do usuário.')
        async def saldo(interaction: discord.Interaction, nome: str):

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
            embed = discord.Embed(description=f"💸 Saldo {nome}:\n```R$: {saldo}\n```", color=cor)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        
        self.tree = tree

    async def on_ready(self):
        await self.tree.sync(guild=discord.Object(id=id_do_servidor))
        self.synced = True
        print(f"Entremos como {self.user}.")

aclient = client()
aclient.run('MTA4NzE5NTE5MjI5OTM2ODQ0OA.G0wDOj.H60UJ944AP-2Q6kN-QcrozUVBsYTDjesAx74_k')
