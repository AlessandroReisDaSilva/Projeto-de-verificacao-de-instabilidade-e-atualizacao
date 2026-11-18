import requests
import time
import json
from datetime import datetime
import winsound
import os
from dotenv import load_dotenv
load_dotenv()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
url = os.getenv("pagina")
selecao = os.getenv("selecao")
ntfy = os.getenv("ntfy")
discord = os.getenv("discord")
tituloNTFY = os.getenv("tituloNTFY")
modo = os.getenv("modo")

def ntfy_notificar(texto):
    requests.post(f"https://ntfy.sh/{ntfy}", data=texto.encode("utf-8"), headers={"Title": tituloNTFY}, timeout=10)

def discord_notificar(texto):
    mensagem = {
    'text': f"{texto}"
    }
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    requests.post(discord, data=json.dumps(mensagem), headers=headers)

def enviar_notificacao(texto):
    if str(modo).upper() == "NTFY":
        ntfy_notificar(texto)
    else:
        discord_notificar(texto)

def verificar_atualizacao():
    configuracoes = Options()
    configuracoes.add_argument("--headless=new")
    driver = webdriver.Chrome(options=configuracoes)
    driver.get(url)
    conteudo2 = ""
    conteudo = driver.find_elements(by=By.CSS_SELECTOR, value=selecao)
    driver.quit()
    while True:
        try:
            resposta = requests.get(url,timeout=10)
            # print(resposta.status_code)
            if resposta.status_code == 200:
                driver = webdriver.Chrome(options=configuracoes)
                driver.get(url)
                conteudo2 = driver.find_elements(by=By.CSS_SELECTOR, value=selecao)
                # print("seleção1:")
                # print(conteudo[0])
                # print("seleção2:")
                # print(conteudo2[0])
                if conteudo[0] != conteudo2[0]:
                    conteudo = driver.find_elements(by=By.CSS_SELECTOR, value=selecao)
                    print(f"Foi atualizado. | {datetime.now()}")
                    enviar_notificacao(f"Foi atualizado. | {datetime.now()}")
                    winsound.Beep(1000, 200)
                    winsound.Beep(900, 200)
                    winsound.Beep(1000, 100)
                    winsound.Beep(900, 100)
                else:
                    print(f"Não foi atualizado. | {datetime.now()}")
            else:
                verificar_página_online()
                break
            driver.quit()
        except requests.exceptions.RequestException:
            verificar_página_online()
            break
        time.sleep(1)    


def verificar_página_online():
    while True:
        try:
            resposta = requests.get(url,timeout=10)
            # print(resposta.status_code)
            if resposta.status_code == 200:
                print(f"{url} voltou | {datetime.now()}")
                enviar_notificacao(f"{url} voltou | {datetime.now()}")
                winsound.Beep(1000, 200)
                winsound.Beep(900, 200)
                winsound.Beep(1000, 100)
                winsound.Beep(900, 100)
                verificar_atualizacao()
                break
            else:
                print(f"{url} parou de responder! | {datetime.now()}")
        except requests.exceptions.RequestException:
            print(f"{url} parou de responder! | {datetime.now()}")
        time.sleep(1)

verificar_página_online()