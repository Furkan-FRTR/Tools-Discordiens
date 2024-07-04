import requests
import time
from colorama import Fore

def getheaders(token):
    return {
        'Authorization': token,
        'Content-Type': 'application/json'
    }

y = Fore.YELLOW
w = Fore.WHITE
b = Fore.BLUE
r = Fore.RED

def MassDM(token, channels, message, delay):
    contacted_users = set()
    message_count = 0
    for channel in channels:
        for user in [x["username"] + "#" + x["discriminator"] for x in channel["recipients"]]:
            if user not in contacted_users:
                try:
                    print(f"Message envoyé à : {user}")
                    contacted_users.add(user)
                    message_count += 1
                    print(f"Messages envoyés : {message_count}")
                    requests.post(f"https://discord.com/api/v9/channels/{channel['id']}/messages", headers={'Authorization': token}, data={"content": f"{message}"})
                    time.sleep(delay)
                except Exception as e:
                    print(f"Une erreur s'est produite lors de l'envoi à {user}: {e}")

def start_mass_dm():
    token = input(f"{y}Entrez votre token Discord : ")
    message = input(f"{b}Entrez le message à envoyer : ").strip()
    delay = 2
    
    validityTest = requests.get('https://discordapp.com/api/v6/users/@me', headers={'Authorization': token, 'Content-Type': 'application/json'})
    if validityTest.status_code != 200:
        print(f"{r}Token invalide")
        return
    
    channelIds = requests.get("https://discord.com/api/v9/users/@me/channels", headers=getheaders(token)).json()
    if not channelIds:
        print(f"{r}Ce compte n'a pas de messages privés")
        return
    
    MassDM(token, channelIds, message, delay)

print(f"""{r}
============ Mass DM Friend ============
      """)
start_mass_dm()

# by Furkan-FRTR