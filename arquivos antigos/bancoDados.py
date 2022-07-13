import mysql.connector


class Conexao():

    def __init__(self) -> None:

        self.Host = 'localhost'
        self.DataBase = 'bd_atos'
        self.User = 'root'
        self.Pass = '1234'

    # Cria a conexão com o banco de dados
    def conectarBanco(self):

        # Cria a conexão
        self.conexao = mysql.connector.connect(
            host=self.Host, database=self.DataBase, user=self.User, password=self.Pass)

        # Se houve uma conexão retorne ela
        if self.conexao.is_connected():
            return self.conexao

    # Fecha a conexão com o banco de dados
    def fecharConexao(self):

        # Verifica se ainda existe uma conexão se existir fecha a conexão
        if self.conexao.is_connected():
            self.conexao.close()


class InsertBD():

    def __init__(self):
        # Pega a intância de conexão com o banco de dados
        self.bancoDados = Conexao()

    # Insere os horários para notificar o usuário
    def insertDados(self, idJogo: int, jogadorA: str, jogadorB: str, timeA: str, timeB: str, resultadoGols: str,
                    data: str, liga: str):
        conexao = self.bancoDados.conectarBanco()

        # Cria o cursor
        cursor = conexao.cursor()

        COLUNAS = 'idJogo,jogadorA,jogadorB,timeA,timeB,resultadoGols,data,liga'
        VALORES = f"{idJogo},'{jogadorA}','{jogadorB}','{timeA}','{timeB}','{resultadoGols}','{data}','{liga}'"
        SQL = f"INSERT INTO  bd_atos.dados({COLUNAS}) VALUES ({VALORES});"

        # Exucuta a instrução sql
        cursor.execute(SQL)

        # Grava no banco
        conexao.commit()

        # Fecha a conexão
        conexao.close()

    # Insere os horários para notificar o usuário
    def insertDadosFuturo(self, jogadorA: str, jogadorB: str, timeA: str, timeB: str,
                          data: str, liga: str):
        conexao = self.bancoDados.conectarBanco()

        # Cria o cursor
        cursor = conexao.cursor()

        COLUNAS = 'jogadorA,jogadorB,timeA,timeB,data,liga'
        VALORES = f"'{jogadorA}','{jogadorB}','{timeA}','{timeB}','{data}','{liga}'"
        SQL = f"INSERT INTO  bd_atos.dadoJogosFuturos({COLUNAS}) VALUES ({VALORES});"

        # Exucuta a instrução sql
        cursor.execute(SQL)

        # Grava no banco
        conexao.commit()

        # Fecha a conexão
        conexao.close()


class SelectBD():

    def __init__(self):
        # Pega a intância de conexão com o banco de dados
        self.bancoDados = Conexao()

    # Seleciona apenas os que não foram notificado
    def selectJogo(self, idJogo: int, opcao: int):
        # Cria a conexão
        conexao = self.bancoDados.conectarBanco()

        # Cria o cursor
        cursor = conexao.cursor()

        if opcao == 1:
            # Exucuta a instrução sql
            cursor.execute(f"SELECT idJogo FROM  bd_atos.dados WHERE idJogo={idJogo};")

        resultados = cursor.fetchone()

        return resultados

    # Seleciona apenas os que não foram notificado
    def selectJogoFuturos(self, jogadorA: str, jogadorB: str, timeA: str, timeB: str, data: str, liga: str):
        jogadorA = jogadorA.replace('ECF_', '')
        jogadorB = jogadorB.replace('ECF_', '')
        # Cria a conexão
        conexao = self.bancoDados.conectarBanco()

        # Cria o cursor
        cursor = conexao.cursor()

        # Exucuta a instrução sql
        cursor.execute(
            f"SELECT jogadorA FROM  bd_atos.dadoJogosFuturos WHERE jogadorA='{jogadorA}' AND jogadorB='{jogadorB}' AND timeA='{timeA}' AND timeB='{timeB}' AND data='{data}' AND liga='{liga}';")

        resultados = cursor.fetchone()

        return resultados

    def selectJogos(self, jogadorA: str, jogadorB: str):
        jogadorA = jogadorA.replace('ECF_','')
        jogadorB = jogadorB.replace('ECF_', '')

        # Cria a conexão
        conexao = self.bancoDados.conectarBanco()

        # Cria o cursor
        cursor = conexao.cursor()

        # Exucuta a instrução sql
        cursor.execute(
            f"SELECT * FROM bd_atos.dados WHERE jogadorA='{jogadorA}' and jogadorB='{jogadorB}' OR jogadorA='{jogadorB}' and jogadorB='{jogadorA}';")

        resultados = cursor.fetchall()

        return resultados

    def selectJogosPorData(self, jogadorA: str, jogadorB: str, data: str):
        jogadorA = jogadorA.replace('ECF_', '')
        jogadorB = jogadorB.replace('ECF_', '')
        # Cria a conexão
        conexao = self.bancoDados.conectarBanco()

        # Cria o cursor
        cursor = conexao.cursor()

        # Exucuta a instrução sql
        cursor.execute(
            f"SELECT * FROM bd_atos.dados WHERE  data LIKE ('{data}%') and jogadorA='{jogadorA}' and jogadorB='{jogadorB}' OR  data LIKE ('{data}%') and  jogadorA='{jogadorB}' and jogadorB='{jogadorA}';")

        resultados = cursor.fetchall()

        return resultados

    def selectJogosPorTime(self, jogadorA: str, timeA: str, jogadorB: str, timeB: str):
        jogadorA = jogadorA.replace('ECF_', '')
        jogadorB = jogadorB.replace('ECF_', '')

        # Cria a conexão
        conexao = self.bancoDados.conectarBanco()

        # Cria o cursor
        cursor = conexao.cursor()

        # Exucuta a instrução sql
        cursor.execute(
            f"SELECT * FROM bd_atos.dados WHERE jogadorA='{jogadorA}' and timeA='{timeA}' and jogadorB='{jogadorB}' and timeB='{timeB}' or jogadorA='{jogadorB}' and timeA='{timeB}' AND jogadorB='{jogadorA}' and timeB='{timeA}';")

        resultados = cursor.fetchall()

        return resultados

    # Seleciona apenas os que não foram notificado
    def selectDadosPeriodo(self, data: str):
        # Cria a conexão
        conexao = self.bancoDados.conectarBanco()

        # Cria o cursor
        cursor = conexao.cursor()

        # Exucuta a instrução sql
        cursor.execute(f"SELECT * FROM bd_atos.dadoJogosFuturos WHERE data LIKE ('{data}%');")

        resultados = cursor.fetchall()

        return resultados
