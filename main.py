'''
    DROOM -
        Client_ID_DROOM = '3d824385cf984bd78eece82d741f3b7a'
        Client_Secret_DROOM = 'mgAJkZVXhpnHYMDsKn6BHMb_P0rWnJe-EYgsAM16rSkHj5-6QNwv2f4QZ5iTn8Fk3peO1YB2kiBoz4jYaOPtSQ'
        Autorização = basic YTVjOWZhYjdkMDcwNGY5MDhiNDhlMDM3YmFmM2IyMDY6V1dNQnNrSmU3RTZhUWhJdzNxNXRrNkRvUnRfWUJ0dVNzNEVDcmt6aDkwVUc1ZTNKMm9vbVRfMWVrSUVrZ3Nrc1hMOEtqbWRyZWtWa0RMai1SOVhYNFE=
'''

import requests
from datetime import datetime
import base64
import json
import time

def data_formatada():
    data_hoje = datetime.now().date()
    data_formatada = f"{data_hoje}T00:00:00"
    return data_formatada
def Request(data_hoje,Fila,em_pausa,logados,disponivel,em_atendimento):
    url_request = "http://192.168.5.62:8091/BCMS_WEB/api/v1/Integracao/ReportTempoReal/Gravar"
    try:
        '''REQUEST VOZ '''
        DROOM = '{"Operacao": {"Constante": "RIO_CORPORATE"}, "DataRegistro": "' + f'{data_hoje}' + '", "DataEvento": "' + f'{data_hoje}' + '", "Grupo": "100", "NomeGrupo": "DROOM", "ChamadaEspera": "' + f'{Fila}' + '", "NivelServico": "0", "Logado": "' + f'{logados}' + '", "Disponivel": "' + f'{disponivel}' + '", "Acd": "' + f'{em_atendimento}' + '", "Acw": "' + f'{em_pausa}' + '", "Aux": "0", "SaidaRamal": "0", "Outro": "0", "ChamadaAntiga": "0",\"Itens\": []}'
        headers = {
          'content-type': "application/json",
          'cache-control': "no-cache",
          'postman-token': "9e904e79-6ef2-4feb-416c-e1c2b410be09"
        }
        DROOM_request = requests.request("POST", url_request, data=DROOM, headers=headers)
        print(f"Droom Request - {DROOM_request.status_code} ")
        print(" ")
    except Exception as A:
            print(A)
def Requisica0_Token():
    '''Client_ID_DROOM = '3d824385cf984bd78eece82d741f3b7a'
    Client_Secret_DROOM = 'mgAJkZVXhpnHYMDsKn6BHMb_P0rWnJe-EYgsAM16rSkHj5-6QNwv2f4QZ5iTn8Fk3peO1YB2kiBoz4jYaOPtSQ'
    Autorizacao = base64.b64encode(bytes(f'{Client_ID_DROOM}:{Client_Secret_DROOM}', "UTF-8"))
    print(Autorizacao)'''

    URL_API = "https://droom.talkdeskid.com/oauth/token"
    payload = {"grant_type": "client_credentials"}
    headers = {
        "accept": "application/json",
        "Authorization": "Basic M2Q4MjQzODVjZjk4NGJkNzhlZWNlODJkNzQxZjNiN2E6bWdBSmtaVlhocG5IWU1Ec0tuNkJITWJfUDByV25KZS1FWWdzQU0xNnJTa0hqNS02UU53djJmNFFaNWlUbjhGazNwZU8xWUIya2lCb3o0allhT1B0U1E=",
        "content-type": "application/x-www-form-urlencoded"
    }
    response = requests.post(URL_API, data=payload, headers=headers)
    data = json.loads(response.text)
    #print(data)
    access_token = data['access_token']
    return  access_token
def Extracao_Usuarios(tolken):
    url = "https://api.talkdeskapp.com/live-subscriptions"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tolken}",
        "content-type": "application/json"
    }

    #Status Usuário
    body_status_users = {
        "queries": [
            {
                "id": f"{TALK_DIC['id_live_users']}",
                "metadata": {
                    "name": f"{TALK_DIC['nome_live_users']}"
                },
                "params": {},
                "filters": {"range": {"from": f"{data_formatada()}"}},
            }
        ]
    }
    response_status_users = requests.post(url, headers=headers, json=body_status_users)
    data = json.loads(response_status_users.text)
    stream_href_url_status_users = data['_links']['stream']['href']
    with (requests.get(stream_href_url_status_users, stream=True) as response_status_users):
        for chunk in response_status_users.iter_content(chunk_size=1000):
            if chunk:
                Result_fila = chunk.decode("utf-8")
                dados_json = json.loads(Result_fila.split("data:")[1])
                em_pausa = 0
                logados = 0
                disponivel = 0
                em_atendimento = 0

                for item in dados_json["result"]:
                    nome = item["_key"]
                    valor = int(item["_value"])  # Converte o valor para inteiro

                    if nome == "away" or nome == "away_ambulatrio" or nome == "away_ativo" or nome == "away_backoffice" or nome == "away_banheiro" or nome == "away_descanso" or nome == "away_lanche" or nome == "away_reunio":
                        em_pausa += valor
                    elif nome == "_total":
                        logados += valor
                    elif nome == "available":
                        disponivel += valor
                    elif nome == "after_call_work" or nome == "busy":
                        em_atendimento += valor
                pass
                break
    return  (em_pausa, logados,disponivel,em_atendimento)
def Extracao_Fila(tolken):
    url = "https://api.talkdeskapp.com/live-subscriptions"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tolken}",
        "content-type": "application/json"
    }

    body_fila = {
        "queries": [
            {
                "id": f"{TALK_DIC['id_fila']}",
                "metadata": {
                    "name": f"{TALK_DIC['nome_fila']}"
                },
                "params": {},
                "filters": {"range": {"from": f"{data_formatada()}"}},
            }
        ]
    }
    response_fila = requests.post(url, headers=headers, json=body_fila)
    data = json.loads(response_fila.text)
    stream_href_url_fila = data['_links']['stream']['href']
    with requests.get(stream_href_url_fila, stream=True) as response_fila:
        for chunk in response_fila.iter_content(chunk_size=128):
            if chunk:
                Result_fila = chunk.decode("utf-8")
                indice_result = Result_fila.find('"result":')
                substring = Result_fila[indice_result:]
                indice_colchete_aberto = substring.find('[')
                indice_colchete_fechado = substring.find(']')
                resultado_substring = substring[indice_colchete_aberto:indice_colchete_fechado + 1]
                resultado_json = json.loads(resultado_substring)
                Fila = resultado_json[0]['_value']
                break
    return Fila

def Get_Last_Data(Pausa,Logados,Disponivel,Em_atendimento,Fila):
    data_hoje = datetime.now()
    ultimo_update = f"{data_hoje}"
    ultima_Pausa = Pausa
    ultimo_Logado = Logados
    ultimo_Disponivel = Disponivel
    ultimo_Em_Atendimento = Em_atendimento
    ultima_Fila = Fila
    return ultima_Pausa,ultimo_Logado,ultimo_Disponivel,ultimo_Em_Atendimento,ultimo_update, ultima_Fila

# DICIONÁRIO
TALK_DIC = {
    "nome_fila": "live_contacts_in_queue",
    "id_fila": "2fbf3f809fca4352a5b458da347a6f9f",
    "nome_tempo_atendimento": "avg_handle_time",
    "id_tempo_atendimento": "35267ca0b4c6410895ddd45ad4043a0e",
    "nome_nivel_servico": "service_level",
    "id_nivel_serivco": "ab8e693f64d741e081d117197929c2d9",
    "nome_live_users": "live_users_logged_in_by_status",
    "id_live_users": "2d3f540ccecb4776902bd317fe2e411d",
    "nome_Tempo__Médio_Espera": "avg_wait_time_by_ring_group",
    "id_Tempo_Médio_Espera": "7c9178ff86eb4b51ad86f75f3fc5cfe4",
    "nome_Maior_Tempo_Espera": "longest_wait_time_by_ring_group",
    "id_Maior_Tempo_Espera": "645cb1fe79a244a9a151592453d66c78",
    "nome_ligacoes_atendidas": "answered_contacts",
    "id_ligacoes_atendidas": "4e9788986d6845cd8f0d25d31f849bdf",
    "nome_ligacoes_perdidas": "missed_contacts",
    "id_ligacoes_perdidas": "91d2e348dbd64c4a8dde729356575c5d",
    "nome_ligacoes_total": "inbound_contacts",
    "id_ligacoes_total": "b7c50e0ae810452181a1d7c7f14cf8ba",
}

i = True
while i ==  True:
    try:
            data_atual = data_formatada()
            token  = Requisica0_Token()
            Pausa, Logados, Disponivel, Em_atendimento = Extracao_Usuarios(token)
            Fila = Extracao_Fila(token)
            ultima_Pausa, ultimo_Logado, ultimo_Disponivel, ultimo_Em_Atendimento, ultimo_update, ultima_Fila = Get_Last_Data(Pausa,Logados,Disponivel,Em_atendimento, Fila)
            print(f'Em pausa: {Pausa}')
            print(f'Logados: {Logados}')
            print(f'Disponível: {Disponivel}')
            print(f"Em atendimento: {Em_atendimento}")
            print(f"Fila: {Fila}")
            print(f" ")
            Request(data_atual, Fila, Pausa, Logados, Disponivel, Em_atendimento)
            time.sleep(10)

    except:
        tempo = 30
        Pausa = ultima_Pausa
        Logados = ultimo_Logado
        Disponivel = ultimo_Disponivel
        Em_atendimento = ultimo_Em_Atendimento
        Fila = ultima_Fila
        data_atual = ultimo_update

        print("Aguardando....", tempo)
        print("ULTIMO UPDATE :", ultimo_update)
        print("Ultima 'Fila':", ultima_Fila)
        print(f"Ultima 'Pausa': ", ultima_Pausa)
        print(f"Ultimo 'Logados': ", ultimo_Logado)
        print(f"Ultimo 'Disponivel': ", ultimo_Disponivel)
        print(f"Ultimo 'Em atendimento': ", ultimo_Em_Atendimento)
        print("")
        Request(data_atual, Fila, Pausa, Logados, Disponivel, Em_atendimento)
        time.sleep(tempo)
        tempo += 60