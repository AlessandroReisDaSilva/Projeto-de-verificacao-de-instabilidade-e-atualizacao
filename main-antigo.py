import requests
import time
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

def verificar2():
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
                # print(conteudo2)
                if conteudo != conteudo2:
                    conteudo = driver.find_elements(by=By.CSS_SELECTOR, value=selecao)
                    print(f"Foi atualizado. | {datetime.now()}")
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
                winsound.Beep(1000, 200)
                winsound.Beep(900, 200)
                winsound.Beep(1000, 100)
                winsound.Beep(900, 100)
                verificar2()
                break
            else:
                print(f"{url} parou de responder! | {datetime.now()}")
        except requests.exceptions.RequestException:
            print(f"{url} parou de responder! | {datetime.now()}")
        time.sleep(1)

verificar_página_online()