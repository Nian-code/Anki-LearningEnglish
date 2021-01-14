import requests
from bs4 import BeautifulSoup
import main

def ingles_example(word):
    url = f'https://www.ingles.com/traductor/{word}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    english = soup.select("._1f2Xuesa")
    spanish = soup.select("._3WrcYAGx")
    for en, es in zip(english, spanish):
        print(en.text, "\n", es.text)
    if not english:
        print("Word not find")

