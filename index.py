import requests
from bs4 import BeautifulSoup
import os
import yt_dlp
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

try:
    print("Preparando o ambiente...")
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    servico = Service(ChromeDriverManager().install())
    options.add_argument('--headless')
    options.add_argument("--log-level=3")
    navegador = webdriver.Chrome(service=servico, options=options)
    navegador.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    os.system("cls || clear")
except:
    print("[ERRO] -> Instalação e configuração dos requisitos falhou, reporte!")

def baixar_a_aula(ntemporada, episodio, link, anime):
    navegador.get(link)
    k = navegador.find_element(By.XPATH, '//*[@id="dooplay_player_response"]/div/iframe')
    attr = k.get_attribute('src')
    if not os.path.exists(anime):
        os.makedirs(anime)
    if os.path.exists(f"{anime}/Temporada {ntemporada}/{episodio}/{episodio}.mp4"):
        print(f'{episodio} da temporada {ntemporada} já baixado, pulando...')
    else:
        os.system("cls || clear")
        ydl_opts = {"format": "best",
                    'retries': 9,
                    'fragment_retries': 9,
                    'quiet': True,
                    "outtmpl": f"{anime}/Temporada {ntemporada}/{episodio}/{episodio}.mp4"}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download(attr)
        except:
            print("Deu um erro com o link, reporte!")


def pegar_temporada(seasons, anime):
    t = seasons.find_all('div', {'class': 'se-c'})
    for i in t:
        temporada = i.contents[0].text[0]
        temps = i.find_all('li')
        for r in temps:
            ep = r.find('a').text
            href = r.find('a')['href']
            baixar_a_aula(temporada, ep, href, anime)
        
def main():
    os.system('cls || clear')
    site = input('Digite a URL do anime: ')
    r = requests.get(site).text
    soup = BeautifulSoup(r, 'html.parser')
    seasons = soup.find('div', {'id': 'seasons'})
    anime = soup.find('div', {'class', 'data'}).contents[1].text
    if ':' in anime:
        anime = anime.replace(":", "-")
    if '\\' in anime:
        anime = anime.replace("\\", "-")
    if '/' in anime:
        anime = anime.replace("/", "-")
    if '|' in anime:
        anime = anime.replace("|", "-")
    if '>' in anime:
        anime = anime.replace(">", "-")
    if '<' in anime:
        anime = anime.replace("<", "-")
    if '*' in anime:
        anime = anime.replace("*", "-")
    if '"' in anime:
        anime = anime.replace('"', "-")
    if '?' in anime:
        anime = anime.replace("?", "-")
    print("Verificando... Aguarde!")
    pegar_temporada(seasons, anime)

main()