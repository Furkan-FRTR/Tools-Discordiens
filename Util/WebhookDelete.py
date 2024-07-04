import os
import requests
from colorama import Fore

def setTitle(title):
    os.system(f"title {title}")

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def webhremovertitle():
    print(f"{Fore.YELLOW}-----------------------------")
    print(f"{Fore.WHITE}        WebHook delete        ")
    print(f"{Fore.YELLOW}-----------------------------")

def main():
    clear()
    webhremovertitle()
    webhooksremover()

def webhooksremover():
    try:
        webhook = input(f"{Fore.WHITE}Entrez le lien du WebHook à supprimer : ")
        if not webhook:
            print(f"{Fore.RED}Erreur : Le lien du WebHook ne peut pas être vide.")
            return
        confirm = input(f"{Fore.YELLOW}Voulez-vous vraiment supprimer ce WebHook ? (o/n) : ").lower()
        if confirm != 'o':
            print(f"{Fore.YELLOW}Opération annulée.")
            return
        response = requests.delete(webhook.strip())
        if response.status_code == 204:
            print(f"{Fore.GREEN}Le Webhook a été supprimé avec succès.")
        else:
            print(f"{Fore.RED}Échec de la suppression du Webhook. Code d'état : {response.status_code}")
    except requests.exceptions.MissingSchema:
        print(f"{Fore.RED}Erreur : Le lien du WebHook est invalide.")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Erreur lors de la requête : {e}")
    except Exception as e:
        print(f"{Fore.RED}Une erreur s'est produite : {e}")
    input(f"{Fore.WHITE} Appuyez sur ENTREE pour quitter")

if __name__ == "__main__":
    main()

# by Furkan-FRTR