import requests
import time
from colorama import Fore
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

y = Fore.YELLOW
w = Fore.WHITE
b = Fore.BLUE
r = Fore.RED

def main():
    print(f"{y}=====================")
    print(f"{b}===== AutoLogin =====")
    print(f"{y}=====================")

    print(f"{w}Entrez le token du compte auquel vous souhaitez vous connecter")
    entertoken = str(input(f"{b}Token : "))
    
    validityTest = requests.get('https://discordapp.com/api/v6/users/@me', headers={'Authorization': entertoken, 'Content-Type': 'application/json'})
    
    if validityTest.status_code != 200:
        print(f"\n{r}Token invalide")
        input(f"""\n{y}Appuyez sur ENTREE pour quitter""")
        return
    
    try:
        driver_service = ChromeService(executable_path=r'util/chromedriver.exe')
        driver = webdriver.Chrome(service=driver_service)
        driver.maximize_window()
        driver.get('https://discord.com/login')
        
        js = 'function login(token) {setInterval(() => {document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`}, 50);setTimeout(() => {location.reload();}, 500);}'
        
        time.sleep(3)
        driver.execute_script(js + f'login("{entertoken}")')
        time.sleep(10)
        
        if driver.current_url == 'https://discord.com/login':
            print(f"""{r}Connexion échouée""")
            driver.close()
        else:
            print(f"""{b}Connexion établie""")
        
        input(f"""{y}Appuyez sur ENTREE pour quitter""")
    
    except Exception as e:
        print(f"{r}Un problème est survenu : {str(e)}")
        time.sleep(2)
        main()

if __name__ == "__main__":
    main()

# by Furkan-FRTR