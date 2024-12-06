from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def configure_driver():
    # Setează opțiuni pentru Chrome
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")  # Dezactivează GPU
    chrome_options.add_argument("--no-sandbox")  # Previne erorile la rularea în anumite medii
    #chrome_options.add_argument("--headless")  # Rulează browserul în mod headless

    # Adaugă un User-Agent pentru a simula un browser real
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")

    proxy_answer = input("Do you want to activate proxy ? : yes/no ").capitalize()
    match proxy_answer:
        case "YES":
            proxy = "113.162.46.233:8080"
            chrome_options.add_argument(f'--proxy-server={proxy}')
            print(f"Starting to search with proxy: {proxy}")
        case "NO":
            print("Starting to search without proxy...")


    # Configurează serviciul și driverul Chrome
    service = Service('./chromedriver.exe')  # Asigură-te că ai chromedriver.exe în folderul corect
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)  # Așteaptă până la 10 secunde pentru elemente
    return driver