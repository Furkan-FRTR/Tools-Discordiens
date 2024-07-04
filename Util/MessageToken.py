import sys
import requests
from colorama import Fore, Style

yellow = Fore.YELLOW
blue = Fore.BLUE
red = Fore.RED
green = Fore.GREEN
reset = Style.RESET_ALL

def get_user_input(prompt):
    return input(f"{blue}{prompt}{reset} : ")

def send_message(token, channel_id, message):
    endpoint = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    payload = {
        "content": message
    }
    response = requests.post(endpoint, headers=headers, json=payload)

if __name__ == "__main__":
    try:
        print(f"{blue}--- MessageToken ---{reset}")
        GUILD_ID = get_user_input("Veuillez saisir l'identifiant du serveur (GUILD_ID)")
        CHANNEL_ID = get_user_input("Veuillez saisir l'identifiant du canal (CHANNEL_ID)")
        usertoken = get_user_input("Veuillez saisir votre token")

        validate = requests.get('https://discordapp.com/api/v9/users/@me', headers={"Authorization": usertoken})
        validate.raise_for_status() 
        print(f"{green}SUCCÈS: Connexion au serveur Discord reussie !{reset}")

        while True:
            message = input(f"{blue}Entrez le message que vous souhaitez envoyer (ou 'exit' pour quitter){reset} : ")
            if message.lower() == 'exit':
                print(f"{red}Arret du script demande.{reset}")
                break
            send_message(usertoken, CHANNEL_ID, message)
    except KeyboardInterrupt:
        print(f"{red}Arret par l'utilisateur.{reset}")
        sys.exit(0)
    except requests.exceptions.RequestException as e:
        print(f"{red}ERREUR: Probleme lors de la requete : {e}{reset}")
        sys.exit(1)

# by Furkan-FRTR