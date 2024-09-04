import selenium.webdriver as webdriver
from selenium.webdriver import Remote, FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import logging
import os

# Load environment variables
load_dotenv()
SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")

FIREFOX_DRIVER_PATH = "./geckodriver"

# Configure logging
logging.basicConfig(filename="scraping.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def scrape_website(website):
    logging.info(f"Tentative de  scraping du site web : {website}")
    print("Connexion au navigateur de scraping...")
    
    firefox_driver_path = FIREFOX_DRIVER_PATH
    options = webdriver.FirefoxOptions()
    
    # Enable headless mode
    options.add_argument("--headless")
    
    driver = webdriver.Firefox(service=Service(firefox_driver_path), options=options)

    try:
        driver.get(website)
        print("La page web a été chargée")
        html = driver.page_source
        logging.info(f"Scraping réussi du site web : {website}")
        return html
    
    except Exception as e:
        logging.error(f"Une erreur s'est produite lors du scraping {website} : {e}")
        print(f"Une erreur s'est produite lors du scraping : {e}")
        return None
    
    finally:
        driver.quit()

def scrape_website_with_proxy(website):
    logging.info(f"Tentative de scraping du site web avec un proxy : {website}")
    print("Connexion au navigateur de scraping...")

    firefox_options = FirefoxOptions()
    
    # Enable headless mode
    firefox_options.add_argument('--headless')

    firefox_service = Service(executable_path=SBR_WEBDRIVER)
    
    try:
        with Remote(command_executor=firefox_service.service_url, options=firefox_options) as driver:
            driver.get(website)
            
            print("Attente de la résolution du captcha...")
            solve_res = driver.execute_script("""
                // Custom script or method to handle captcha in Firefox
                return {status: 'solved'};
            """)
            
            print("Statut de la résolution du captcha : ", solve_res["status"])
            print("Navigation réussie ! Récupération du contenu de la page...")
            html = driver.page_source
            logging.info(f"Scraping réussi du site web avec un proxy : {website}")
            return html
    
    except Exception as e:
        logging.error(f"Error occurred while scraping with proxy {website}: {e}")
        print(f"Une erreur s'est produite lors de la scraping avec un proxy : {e}")
        return None

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
