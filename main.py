import ipa
import translator
import polly
import example
import yaml
import sys

def solicitud():
    word = str(input("Ingresa una palabra: ")).lower()
    if not word:
        solicitud()
    return word

def config_def():
    with open("config.yaml") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        f.close
    return config

def choise_options(config, word):
    if config["ipa"]["wikitionary"] and config["ipa"]["lexico"] == 1:
        print("Elije solo una opción de ipa")
    elif config["ipa"]["CMU"] and config["ipa"]["wikitionary"] == 1:
        print("Elije solo una opción de ipa")
    elif config["ipa"]["wikitionary"] == 1:
        ipa_response = ipa.wiktionary(word)
        
    elif config["ipa"]["lexico"] == 1: 
        ipa_response = ipa.lexico(word)

    elif config["ipa"]["CMU"] == 1:
        ipa_response = ipa.ipa_cmu(word)
           
    else:
        print("Revisa la configuración en config.yaml sección IPA")
    # Si no hay nada en ipa_response entonces se devuelve al menú
    if not ipa_response:
        run()

    if config["translator"]["googletranslate"] and config["translator"]["linguee"] == 1:
        print("Revisa la configuración en config.yaml, has elegido varios motores de traducción")
    elif config["translator"]["googletranslate"] == 1:
        translator.googletrans(word)

    elif config["translator"]["linguee"] == 1:
        translator.linguee(word)
    else:
        print("Revisa la configuración en config.yaml sección translate")

    example.ingles_example(word)
    polly.generate_sound(word)

def run():
    config = config_def()
    word   = solicitud()
    choise_options(config, word)

if __name__ == "__main__":
    run()