import requests
import json
from datetime import datetime
from bancoDados import InsertBD, SelectBD
from dateutil.relativedelta import relativedelta

# Pega a hora de notificar
def getYour(your: str):

    # concatena a hora atual + o minuto de aposta e subtrai 2 minutos
    your = datetime.strptime(your, '%d/%m/%Y %H:%M')

    # Monta hora que deve aposta
    your = datetime.strftime(your + relativedelta(hours=-4), '%d/%m/%Y %H:%M')

    return your

def gravar08minutos(data : str):

    dateFrom = f'{data[6:10]}%2F{data[3:5]}%2F{data[0:2]}+04%3A00'
    dateTo = f'{data[6:10]}%2F{data[3:5]}%2F{int(data[0:2])+1}+03%3A59'
    URL = f'https://football.esportsbattle.com/api/tournaments?page=1&dateFrom={dateFrom}&dateTo={dateTo}'

    dados = json.loads(requests.get(URL).text)
    paginas = int(dados['totalPages'])

    pagina = 1
    while pagina <= paginas:
        URL = f'https://football.esportsbattle.com/api/tournaments?page={pagina}&dateFrom={dateFrom}&dateTo={dateTo}'
        linhas = json.loads(requests.get(URL).text)['tournaments']

        for linha in linhas:
            page = json.loads(requests.get(f"https://football.esportsbattle.com/api/tournaments/{linha['id']}/matches").text)

            for lin in page:

                your = str(lin['date']).replace('T', ' ').replace('Z', '').replace('-', '/')
                your = getYour(datetime.strptime(your, '%Y/%m/%d %H:%M:%S').strftime('%d/%m/%Y %H:%M'))
                player_01 = lin['participant1']['nickname']
                player_02 = lin['participant2']['nickname']
                team_01 = lin['participant1']['team']['token_international']
                team_02 = lin['participant2']['team']['token_international']

                if SelectBD().selectJogoFuturos(player_01, player_02, team_01, team_02, your, '08 Minutos') == None:
                    InsertBD().insertDadosFuturo(player_01, player_02, team_01, team_02, your, '08 Minutos')
                    print('--------------------')
                    print(your, ' | ', player_01, ' | ', team_01)
                    print(your, ' | ', player_02, ' | ', team_02)
        pagina += 1

