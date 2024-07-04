import subprocess
import sys
from colorama import init, Fore, Style
import colorama
import os

init(autoreset=True)

options = [
    "MassDMFriend", "NitroGen", "TokenChecker", 
    "TokenInfo", "VocToken", "WebhookDelete",
    "WebhookSpam", "Autologin", "SelfBot"
]

info_option = "Info"

colorama.init(autoreset=True)

def draw_menu():
    drawing = [
        r"   _____ _   _ ____  _  __    _    _   _  ",
        r"  |  ___| | | |  _ \| |/ /   / \  | \ | | ",
        r"  | |_  | | | | |_) | ' /   / _ \ |  \| | ",
        r"  |  _| | |_| |  _ <| . \  / ___ \| |\  | ",
        r"  |_|    \___/|_| \_\_|\_\/_/   \_\_| \_| "
    ]
    
    colors = [Fore.LIGHTYELLOW_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTWHITE_EX]
    
    for index, line in enumerate(drawing):
        print(colors[index % len(colors)] + Style.BRIGHT + line.center(60))

    print("\n" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + "Sélectionnez une option".center(60) + "\n")

    col1 = options[:3]
    col2 = options[3:6]
    col3 = options[6:9]

    for i in range(3):
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + f"{i+1}. {col1[i]}".ljust(20) + 
              Fore.LIGHTGREEN_EX + Style.BRIGHT + f"{i+4}. {col2[i]}".ljust(20) + 
              Fore.LIGHTGREEN_EX + Style.BRIGHT + f"{i+7}. {col3[i]}".ljust(20))

    print("\n" + Fore.LIGHTMAGENTA_EX + Style.BRIGHT + f"10. {info_option}".center(60))

    print("\n" + Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "Tapez le numéro de votre choix et appuyez sur Entrée".center(60))

def main():
    while True:
        draw_menu()
        choice = input("\nVotre choix: ").strip()

        if choice in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10'}:
            if choice == '10':
                script_name = info_option + '.py'
            else:
                script_name = options[int(choice) - 1] + '.py'
            script_path = os.path.join('UTIL', script_name)
            try:
                subprocess.run([sys.executable, script_path])
            except FileNotFoundError:
                print(Fore.RED + f"Script {script_name} introuvable dans le dossier UTIL.")
            break
        else:
            print(Fore.RED + "Choix invalide, veuillez entrer un numéro entre 1 et 10.")
            continue

if __name__ == "__main__":
    main()

# By Furkan-FRTR