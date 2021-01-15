import requests
from bs4 import BeautifulSoup
import eng_to_ipa as engipa
import main


def ipa_requests(url, selector, word):
    url += word
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.select(selector)

    return titles


def cleaner(ipa):
    ipa = ipa.replace("r", "ɹ")
    if not ipa:
        return ipa
    elif "/" not in ipa:
        ipa = "/"+ipa+"/"

    return ipa


def wiktionary(word):
    url = "https://en.wiktionary.org/wiki/"
    selector = "span.ib-content.qualifier-content"

    titles = ipa_requests(url, selector, word)

    if titles:
        type_ipa = []

        for title in titles:
            if title.a and not word in title.text:
                type_ipa.append(title.text)

        if not type_ipa:
            type_ipa.append("IPA")

        ipas_list = ipa_requests(url, "span.IPA", word)
        ipas = [ipa.text for ipa in ipas_list]
        dic = dict(zip(type_ipa, ipas))
        print(dic)
        return dic

    else:
        print("Word not find")
        return None

def lexico(word):
    url = "https://www.lexico.com/en/definition/"
    selector = "span.phoneticspelling"
    titles = ipa_requests(url, selector, word)

    if titles:
        ipa = titles[1].text
        ipa = cleaner(ipa)
        print(ipa)

        try:
            ipa2 = titles[3].text
            ipa2 = cleaner(ipa2)
            if ipa != ipa2:
                print(ipa2)

        except:
            pass

        if not ipa:
            ipa = titles[0].text
            ipa = cleaner(ipa)
            print(ipa)

        return ipa

    else:
        print("Word not find")
        return None



def ipa_cmu(word):
    def palabra(word):
        palabra = engipa.ipa_list(word)
        palabra = cleaner(str(palabra[0]))
        print(palabra)
        return palabra

    def frase(word):
        oracion = engipa.convert(word)
        oracion = cleaner(oracion)
        print(oracion)
        return(oracion)

    word_list = word.split()

    if len(word_list) == 1:
        return palabra(word)
    elif len(word_list) >= 2:
        return frase(word)
    else:
        print("word not find")
        return None
