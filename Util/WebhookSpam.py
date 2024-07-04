import requests
import time
from colorama import Fore
import threading

y = Fore.YELLOW
w = Fore.WHITE
b = Fore.BLUE
r = Fore.RED

def webhspamtitle():
    print(f"{Fore.YELLOW}-----------------------------")
    print(f"{Fore.WHITE}        WebHook Spammer       ")
    print(f"{Fore.YELLOW}-----------------------------")

def webhookspam():
    webhspamtitle()
    print(f"{y} Entrez le lien du WebHook que vous souhaitez spammer : ")
    webhook = input(f"{r} Lien du WebHook: ")
    try:
        requests.post(webhook, json={'content': ""})
    except:
        print(f"{r} Votre WebHook est invalide !")
        time.sleep(2)
    print(f"{y} Entrez le message à spammer : ")
    message = input(f"{r} Message: ")
    print(f"{y} Nombre de messages à envoyer : ")
    amount = int(input(f"{r} Quantité: "))
    def spam():
        requests.post(webhook, json={'content': message})
    for x in range(amount):
        threading.Thread(target=spam).start()
    
    print(f"{b} \nLe WebHook a été correctement spamé")
    input(f"{b}Appuyez sur ENTRÉE pour quitter")

webhookspam()

# by Furkan-FRTR