from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import os

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Load sensitive data from environment variables
company_code = os.getenv("COMPANY_CODE", "a382748")
matricula = os.getenv("MATRICULA", "305284")
password = os.getenv("PASSWORD", "@Agmtech100r")

# Configurações do navegador (Chrome neste caso)
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Inicializa o navegador com o WebDriver Manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Função para realizar o login
def login(driver, company_code, matricula, password):
    try:
        # Acessa o site do Ahgora na página de nova batida
        driver.get("https://www.ahgora.com.br/novabatidaonline/")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Matrícula e senha']"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.ID, "outlined-basic")))
        driver.find_elements(By.ID, "outlined-basic")[0].send_keys(company_code)
        driver.find_elements(By.ID, "outlined-basic")[1].send_keys(matricula)
        driver.find_element(By.ID, "outlined-password").send_keys(password)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Liberar dispositivo']"))).click()
    except Exception as e:
        logging.error(f"Error during login: {e}")
        raise

# Função para registrar o ponto
def registrar_ponto(driver):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//p[text()='ACESSAR VIA SSO']"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Registrar ponto']"))).click()
        logging.info("Ponto batido com sucesso!")
    except Exception as e:
        logging.error(f"Error during registering point: {e}")
        raise

# Chama a função para bater o ponto
def bater_ponto():
    try:
        login(driver, company_code, matricula, password)
        registrar_ponto(driver)
    except Exception as e:
        logging.error(f"Erro ao bater o ponto: {e}")
    finally:
        driver.quit()

# Executa a função
bater_ponto()
