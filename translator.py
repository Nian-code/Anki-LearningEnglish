import main
from googletrans import Translator
from deep_translator import LingueeTranslator
from deep_translator import GoogleTranslator


def solicitud(word):
    translator = Translator()
    language = translator.detect(word)
    language = language.lang

    if type(language) == list:
        if language[0] == "en" or language[0] == "es":
            return language[0]
        else:
            pass
    else:
        if language == "en" or language == "es":
            return language
        else:
            pass

def do_translat(translator, word):
    language = solicitud(word)
    if language == "en":
        dest = "es"
    else:
        dest = "en"
    if translator == LingueeTranslator:
        try:
            translated = translator(source=language, target=dest).translate(
                word, return_all=True)
            return translated

        except:
            print("Error")

    else:
        try:
            translated = translator(source=language, target=dest).translate(word)
            return translated

        except:
            print("Error")

def linguee(word):
    translated = do_translat(LingueeTranslator, word)
    if translated:
        for i in translated:
            print(i.capitalize())

def googletrans(word):
    translated = do_translat(GoogleTranslator, word)
    if translated:
        print(translated.capitalize())
