import os
import pyttsx3
import speech_recognition as sr
import webbrowser
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

class UnsafeAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.check_hostname = False
        context.verify_mode = False
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

requests_session = requests.Session()
requests_session.mount("https://", UnsafeAdapter())

engine = pyttsx3.init("sapi5")
engine.setProperty('voice', engine.getProperty("voices")[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
def getCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ouvindo...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Reconhecendo...")
        command = r.recognize_google(audio, language='pt-br')
        print("Usuário falou:", command)
    except Exception as e:
        print("Erro:", e)
        speak("Não entendi")
        return ""
    return command

def pesquisar_no_google(query):
    speak(f"Pesquisando {query} no Google")
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)

def pesquisar_no_youtube(query):
    speak(f"Pesquisando {query} no YouTube")
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(url)

if __name__ == "__main__":
    speak("Assistente para o Usuário foi ativada")
    speak("Como eu posso te ajudar?")

    while True:
        command = getCommand().lower()
        if command == "":
            continue

        if "assistente" not in command:
            continue
        command = command.replace("assistente", "").strip()

        if 'pesquise no youtube' in command:
            query = command.replace("pesquise no youtube", "").strip()
            pesquisar_no_youtube(query)

        elif 'google' in command and 'pesquise' in command:
            command = command.replace("google", "").replace("pesquise", "").strip()
            pesquisar_no_google(command)

        elif 'youtube' in command:
            speak("Aguarde, abrindo o YouTube")
            webbrowser.open("https://www.youtube.com")
        
        elif 'google' in command:
            speak("Aguarde, abrindo o Google")
            webbrowser.open("https://www.google.com")
        
        elif 'calculadora' in command:
            speak("Aguarde, abrindo a Calculadora")
            os.startfile("C:\\Windows\\System32\\calc.exe")
            
        elif 'visual' in command:
            speak("Aguarde, abrindo o Visual Studio")
            try:
                os.startfile(r"C:\Users\geovanans\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Visual Studio Code")
            except Exception as e:
                print("Erro ao abrir o Visual Studio:", e)
                speak("Não consegui abrir o Visual Studio.")
        
        elif 'tchau' in command or 'sair' in command or 'desligar' in command:
            speak("Até logo")
            break
