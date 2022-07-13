import urllib.request
import json
from datetime import datetime
from bancoDados import InsertBD, SelectBD
from dateutil.relativedelta import relativedelta

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'

def addDay(your : str, qtdDays : int):

    # concatena a hora atual + o minuto de aposta e subtrai 2 minutos
    your = datetime.strptime(your, '%d/%m/%Y')

    # Monta hora que deve aposta
    your = datetime.strftime(your + relativedelta(days=+qtdDays), '%Y-%m-%d')

    return your

# Pega a hora de notificar
def getYour(your: str):

    # concatena a hora atual + o minuto de aposta e subtrai 2 minutos
    your = datetime.strptime(your, '%d/%m/%Y %H:%M')

    # Monta hora que deve aposta
    your = datetime.strftime(your + relativedelta(hours=-4), '%d/%m/%Y %H:%M')

    return your

def gravar12minutos(data : str):

    between = f'between:{addDay(data,0)}T04:00:00.000Z,{addDay(data,1)}T03:59:59.999Z'

    url = f"https://hr.gtleagues.com/api/sports/4/fixtures?kickoff={between}&limit=1000&offset=0&sort=kickoff%2CmatchNr&status=in%3A1%2C0"
    headers = {
        'User-Agent': user_agent,
    }

    request = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(request)
    response = response.read()

    dados = json.loads(response)

    for dado in dados:
        your = str(dado['kickoff']).replace('T', ' ').replace('Z', '').replace('-', '/').replace('.000','')
        your = getYour(datetime.strptime(your, '%Y/%m/%d %H:%M:%S').strftime('%d/%m/%Y %H:%M'))
        player_01 = dado['participants'][0]['participant']['player']['nickname']
        player_02 = dado['participants'][1]['participant']['player']['nickname']
        team_01 = dado['participants'][0]['participant']['team']['name']
        team_02 = dado['participants'][1]['participant']['team']['name']

        if SelectBD().selectJogoFuturos(player_01, player_02, team_01, team_02, your, '12 Minutos') == None:
            InsertBD().insertDadosFuturo(player_01, player_02, team_01, team_02, your, '12 Minutos')
            print('--------------------')
            print(your, ' | ', player_01, ' | ', team_01)
            print(your, ' | ', player_02, ' | ', team_02)

