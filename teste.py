import requests
import json
from bancoDados import SelectBD, InsertBD
from time import sleep
from datetime import datetime
from pytz import timezone

Ligas = ['22614', '22821', '23114']
TOKEN = '126575-eBG7qUJAEIMHlM'

def posicaoCaractere(textoJogador : str, caractere : str):
    indiceLetra = 0
    while indiceLetra <= len(textoJogador):
        if str(textoJogador)[indiceLetra:indiceLetra+1] == caractere:
            return indiceLetra
        indiceLetra += 1

def pegarJogador(textoJogador : str):
    return str(textoJogador)[posicaoCaractere(textoJogador,'(')+1:posicaoCaractere(textoJogador,')')]

def pegarTime(textoJogador : str):
    return str(textoJogador)[0:posicaoCaractere(textoJogador,'(')-1]

def converterData(time : float):
    try:
        timestamp = float(time)
        dt = datetime.fromtimestamp(timestamp, tz=timezone("America/Sao_Paulo"))
        return dt.strftime("%d/%m/%Y %H:%M")
    except ValueError:
        print("não foi possível converter o valor do timestamp para um número")

def liga(liga : str):

    if liga == '22614':
        return '08 Minutos'

    if liga == '22821':
        return '10 Minutos'

    if liga == '23114':
        return '12 Minutos'

while True:

    for league in Ligas:

        pagina = 1
        while pagina <= 1000:

            URL = f'https://api.b365api.com/v3/events/upcoming?sport_id=1&page={pagina}&league_id={league}&token=126575-eBG7qUJAEIMHlM'
            dados = json.loads(requests.get(URL).text)['results']

            if dados == []:
                print('----------------------')
                print(dados)
                break

            try:
                for dado in dados:
                    lista = dict(dado)

                    print(lista)

                    # Pega os dados de cada jogador
                    idJogo = lista['id']
                    timeA = pegarTime(lista['home']['name']).replace("'",'')
                    timeB = pegarTime(lista['away']['name']).replace("'",'')
                    jogadorA = pegarJogador(lista['home']['name']).replace("'",'')
                    jogadorB = pegarJogador(lista['away']['name']).replace("'",'')
                    data = converterData(lista['time'].replace("'", ''))

                    if SelectBD().selectJogo(idJogo,2) == None:
                        InsertBD().insertDados(idJogo, jogadorA, jogadorB, timeA, timeB, '---', data, liga(league))
                        print('==============')
                        print('Dado Gravado')


            except:
                print('-------')
                print(lista['ss'])
                print('Erro')

            pagina += 1
    # Acada loop aguarda 8 minutos
    sleep(480)



