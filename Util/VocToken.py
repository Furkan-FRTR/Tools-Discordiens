import sys
import json
import time
import requests
import asyncio
from colorama import Fore
import websocket
from flask import Flask
from threading import Thread

app = Flask(__name__)

y = Fore.YELLOW
w = Fore.WHITE
b = Fore.BLUE
r = Fore.RED

GUILD_ID = input(f"{b}Veuillez saisir l'identifiant du serveur (GUILD_ID) : ")
CHANNEL_ID = input(f"{b}Veuillez saisir l'identifiant du canal (CHANNEL_ID) : ")
usertoken = input(f"{r}Veuillez saisir votre token : ")

mute_input = input(f"{y}Voulez-vous être en mode muet (Oui/Non) : ")
SELF_MUTE = True if mute_input.lower() == "oui" else False

deaf_input = input(f"{y}Voulez-vous être en mode sourd (Oui/Non) : ")
SELF_DEAF = True if deaf_input.lower() == "oui" else False

status = "online"

headers = {"Authorization": usertoken, "Content-Type": "application/json"}

validate = requests.get('https://discordapp.com/api/v9/users/@me', headers=headers)
if validate.status_code != 200:
    print("[ERROR] Votre token pourrait être invalide. Veuillez le vérifier.")
    sys.exit()

userinfo = validate.json()
username = userinfo["username"]
discriminator = userinfo["discriminator"]
userid = userinfo["id"]

def joiner(token, status):
    ws = websocket.WebSocket()
    ws.connect('wss://gateway.discord.gg/?v=9&encoding=json')
    start = json.loads(ws.recv())
    heartbeat = start['d']['heartbeat_interval']
    auth = {
        "op": 2,
        "d": {
            "token": token,
            "properties": {
                "$os": "Windows 10",
                "$browser": "Google Chrome",
                "$device": "Windows"
            },
            "presence": {
                "status": status,
                "afk": False
            }
        },
        "s": None,
        "t": None
    }
    vc = {
        "op": 4,
        "d": {
            "guild_id": GUILD_ID,
            "channel_id": CHANNEL_ID,
            "self_mute": SELF_MUTE,
            "self_deaf": SELF_DEAF
        }
    }
    ws.send(json.dumps(auth))
    ws.send(json.dumps(vc))
    time.sleep(heartbeat / 1000)
    ws.send(json.dumps({"op": 1, "d": None}))

def run_joiner():
    print(f"Connecté en tant que {username}#{discriminator} ({userid}).")
    while True:
        joiner(usertoken, status)

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == "__main__":
    userinfo = requests.get('https://discordapp.com/api/v9/users/@me',
                            headers={"Authorization": usertoken, "Content-Type": "application/json"}).json()
    username = userinfo["username"]
    discriminator = userinfo["discriminator"]
    userid = userinfo["id"]
    
    keep_alive()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_joiner())

run_joiner()

# by Furkan-FRTR