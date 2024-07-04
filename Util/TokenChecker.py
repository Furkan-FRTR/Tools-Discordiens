import os
import sys
import json
from colorama import Fore

try:
    import aiohttp
    import aiofiles
    import asyncio
    from colorama import Fore, init
except Exception as e:
    print(e)
    os.system(f'{sys.executable} -m pip install -r requirements.txt')
    import aiohttp
    import aiofiles
    import asyncio
    from colorama import Fore, init

init()

config = {"timeout": 500}

y = Fore.YELLOW
w = Fore.WHITE
b = Fore.BLUE
r = Fore.RED
v = Fore.GREEN

state = {
    'invalides': [],
    'valides': [],
    'non vérifiés': []
}

async def verifier_token(token):
    async with aiohttp.ClientSession() as session:
        try:
            headers = {'Authorization': token}
            async with session.get("https://discordapp.com/api/v7/users/@me", headers=headers) as response:
                response.raise_for_status()
                user = await response.json()

                if not user.get('id'):
                    state['invalides'].append(token)
                elif not user.get('verified'):
                    state['non vérifiés'].append(token)
                else:
                    state['valides'].append(token)

        except aiohttp.ClientResponseError as error:
            if error.status == 401:
                state['invalides'].append(token)
        except Exception as error:
            print(f'{error}')

def mettre_a_jour_console():
    mettre_a_jour_titre(f"Valides: {len(state['valides'])} | Non vérifiés: {len(state['non vérifiés'])} | Invalides: {len(state['invalides'])}")
    print(f"{v}Valides: {len(state['valides'])} |{y} Non vérifiés: {len(state['non vérifiés'])} |{r} Invalides: {len(state['invalides'])}")

def mettre_a_jour_titre(titre):
    commande = f'title \"{titre}\"' if os.name == 'nt' else f"\x1b]2;{titre}\x1b\x5c"
    if os.name == 'nt':
        os.system('cls')
        os.system(commande)
    else:
        sys.stdout.write(commande)
        sys.stdout.flush()

async def principal():
    if os.name == 'nt': os.system('cls')
    print(f"{b}Début de la vérification des tokens...")
    if os.name == 'nt': os.system('cls')

    chemin_fichier_tokens = input(f"{y} Veuillez entrer le chemin du fichier contenant les tokens : ").strip()

    if not os.path.exists(chemin_fichier_tokens):
        print(f"{r}Fichier introuvable.")
        return

    async with aiofiles.open('TokensValides.txt', 'w') as fichier_valides:
        async with aiofiles.open(chemin_fichier_tokens, 'r') as f:
            tokens = [line.strip() for line in await f.readlines() if line.strip()]

        if not tokens:
            print(f"{r}Aucun token trouvé dans le fichier.")
            return

        for token in tokens:
            await verifier_token(token)
            mettre_a_jour_console()

        for token_valide in state['valides']:
            await fichier_valides.write(f"{token_valide}\n")

        print(f"{b}Tous les tokens ont été vérifiés, un fichier TokensValides.txt a été créer avec les Token Valide")

if __name__ == '__main__':
    asyncio.run(principal())

# by Furkan-FRTR