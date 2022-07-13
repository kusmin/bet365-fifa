import requests
from bs4 import BeautifulSoup
from bancoDados import InsertBD, SelectBD
from datetime import datetime

__VIEWSTATE = '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'  #pagina.find_all("input", {"id": "__VIEWSTATE"})[0]['value']
__EVENTVALIDATION = 'ob7RDjPsPJXhubJcjFJcESHJGSMe90w52L8UyKLcqqL5r9tqanCrMWuuEgPgUz95/aS5RZi+U8GJGwIy9I12gSSja/3UR2HPIyg3gVErsx6/HmDvFfen7y0IJQoRpZ+8jXLoZAfWSmtc0BmvVCMkZUONwh7ujbktojdBdfPPXYdsP9XIV/B0V9SiQ5sCNT7OstKJYD1xdJ3CkEjXJbBFLo4mU1npN8BMmv74q2nS+Ky3iJ8MEEynDNSO9sDih9MgeBYHrV57z9hWCs56PuGQ2Nwp9uzAfRsWGEZOnBKaCAe3/8R9KfxRU0ScFOtRUc88ysw0Iv5qtrgF+5X0hg8bdLx4uuon3DsbiPtXr1asRM/9sUqK5V1ufaeXvT9BpMIF' #pagina.find_all("input", {"id": "__EVENTVALIDATION"})[0]['value']
__PREVIOUSPAGE = 'iPg5_0kNyc9J73C1-ycA79kMP9kZ9EK50yhEGfUCtLuajvIgcfSguNeAWVeJyNHFZADjYP5nd_lB7okkuvxmSQ2' #pagina.find_all("input", {"id": "__PREVIOUSPAGE"})[0]['value']

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '5257',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'ASP.NET_SessionId=qie2rdhfmd3amwms5ziu3e4z',
    'Host': 'stats.cyberarena.live',
    'Origin': 'https://stats.cyberarena.live',
    'Referer': 'https://stats.cyberarena.live/schedule.aspx',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
}

def gravar10minutos(data : str):
    __DATE = data

    data = {
        '__EVENTTARGET': 'ctl00$MainContent$tb_date',
        '__EVENTARGUMENT': '',
        '__LASTFOCUS': '',
        '__VIEWSTATE': f'{__VIEWSTATE}',
        '__VIEWSTATEGENERATOR': '8E87A3C4',
        '__PREVIOUSPAGE': f'{__PREVIOUSPAGE}',
        '__EVENTVALIDATION': f'{__EVENTVALIDATION}',
        'hdnTimeOffset': '',
        'ctl00$HeaderContent$dd_language': '0',
        'ctl00$MainContent$tb_date': f"{datetime.strptime(__DATE, '%d/%m/%Y').strftime('%Y-%m-%d')}",
        'ctl00$MainContent$dd_utc': '0',
    }

    secao = requests.Session()

    secao.headers.update(header)

    page = secao.get('https://stats.cyberarena.live/schedule.aspx',data=data)

    response = BeautifulSoup(page.content, 'html.parser')

    linhas = response.find_all("tr", {"class": "opacityrow"})

    for linha in linhas:

        colunas = linha.findAll('td')

        your = __DATE + ' ' + colunas[0].text
        team_01 = colunas[1].text
        gamer_Blue = colunas[2].text
        team_02 = colunas[4].text
        gamer_red = colunas[5].text

        if SelectBD().selectJogoFuturos(gamer_Blue, gamer_red, team_01, team_02, your, '10 Minutos') == None:
            InsertBD().insertDadosFuturo(gamer_Blue, gamer_red, team_01, team_02, your, '10 Minutos')
            print('--------------------')
            print(your, ' | ', gamer_Blue, ' | ', team_01)
            print(your, ' | ', gamer_red, ' | ', team_02)

