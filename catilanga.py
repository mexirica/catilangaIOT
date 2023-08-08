import os

from gtts import gTTS
from requests import get
from bs4 import BeautifulSoup
import pygame
import speech_recognition as sr

hotword = "catilanga"

def monitora_audio():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            responde("hello")
            print("Aguardando")
            audio = microfone.listen(source)

            try:
                trigger = microfone.recognize_google(audio, language="pt-br")
                trigger = trigger.lower()

                if hotword in trigger:
                    print(f"Comando: {trigger}")
                    responde("aguarde")
                    executa_comando(trigger)
                    break

            except sr.UnknownValueError:
                responde("entendinada")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return trigger

def responde(nome_audio):
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
    # Inicializar o mixer do pygame
    pygame.mixer.init()

    # Carregar o arquivo de áudio
    pygame.mixer.music.load(f"audios/{nome_audio}.mp3")

    # Reproduzir o áudio
    pygame.mixer.music.play()

    # Aguardar até que o áudio termine de ser reproduzido
    while pygame.mixer.music.get_busy():
        pass

    # Limpar o mixer após a reprodução
    pygame.mixer.quit()

def executa_comando(trigger):
    if "notícias" in trigger:
        ultimas_noticias()

def cria_audio(audio):
    tts = gTTS(audio, lang="pt-br")
    tts.save(f"audios/mensagem.mp3")
    responde("mensagem")

def ultimas_noticias():
    site = get("http://news.google.com/news/rss?need=pt_br&gl=BR&hl=en%E2%80%9D")
    noticias = BeautifulSoup(site.text, "html.parser")
    for noticia in noticias.findAll("item")[:5]:
        mensagem = noticia.title.text
        cria_audio(mensagem)

def main():
    monitora_audio()

if __name__ == '__main__':
    main()

