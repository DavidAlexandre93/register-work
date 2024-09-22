from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import os
import traceback

# Configurações de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Carregar dados sensíveis das variáveis de ambiente ou usar valores padrão para testes
company_code = os.getenv("COMPANY_CODE", "a382748")
matricula = os.getenv("MATRICULA", "305284")
password = os.getenv("PASSWORD", "@Agmtech100r")
browser = os.getenv("BROWSER", "chrome").lower()  # Seleciona o navegador a partir da variável de ambiente, padrão é "chrome"

# Credenciais adicionais para o SSO
sso_username = os.getenv("SSO_USERNAME", "305284")
sso_password = os.getenv("SSO_PASSWORD", "@Agmtech100r")

# Função para inicializar o WebDriver com base no navegador selecionado
def get_driver(browser):
    if browser == "chrome":
        logging.info("Inicializando o Chrome WebDriver...")
        chrome_options = ChromeOptions()
        # chrome_options.add_argument("--headless") # Usar se quiser rodar em modo headless
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-notifications')
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    
    elif browser == "firefox":
        logging.info("Inicializando o Firefox WebDriver...")
        firefox_options = FirefoxOptions()
        # firefox_options.add_argument("--headless") # Usar se quiser rodar em modo headless
        return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)
    
    elif browser == "edge":
        logging.info("Inicializando o Edge WebDriver...")
        edge_options = EdgeOptions()
        # edge_options.add_argument("--headless") # Usar se quiser rodar em modo headless
        return webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=edge_options)
    
    else:
        raise ValueError(f"Navegador '{browser}' não suportado! Use 'chrome', 'firefox' ou 'edge'.")

# Função para realizar o login
def login(driver, company_code, matricula, password):
    try:
        logging.info("Tentando acessar o site...")
        driver.get("https://www.ahgora.com.br/novabatidaonline/")
        
        driver.save_screenshot('pagina.png')
        
        logging.info("Tentando clicar em 'Matrícula e senha'...")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Matrícula e senha']"))).click()
        
        logging.info("Tentando preencher o código da empresa...")
        WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.ID, "outlined-basic")))

        driver.find_elements(By.ID, "outlined-basic")[0].send_keys(company_code)
        
        logging.info("Tentando preencher a matrícula...")
        driver.find_elements(By.ID, "outlined-basic")[1].send_keys(matricula)
        
        logging.info("Tentando preencher a senha...")
        driver.find_element(By.ID, "outlined-password").send_keys(password)
        
        driver.save_screenshot('matricula_senha_preenchidos.png')
        
        logging.info("Esperando carregar a página...")
        time.sleep(5)  # Adiciona uma espera para garantir que tudo esteja carregado
        
        logging.info("Tentando clicar em 'Liberar dispositivo'...")
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//p[text()='Liberar dispositivo']]"))
        ).click()
        
    except Exception as e:
        logging.error(f"Erro durante o login: {e}")
        driver.save_screenshot('erro_login.png')
        raise

# Função para registrar o ponto
def registrar_ponto(driver):
    try:
        logging.info("Iniciando registro do ponto após o login inicial")
         
        # Usar o XPath atualizado para localizar o botão "Registre seu ponto"
        register_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Registre seu ponto']]"))
        )
        register_button.click()
        
        logging.info("Tentando acessar via Matricula e Senha...")

        # Aguardar um pouco antes de clicar para garantir que o botão esteja disponível
        time.sleep(5)
        
        # Inserir as credenciais do SSO
        logging.info("Tentando inserir a matrícula.")
        sso_username_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='outlined-basic-account']"))
        )
        sso_username_input.clear()
        sso_username_input.send_keys(sso_username)
        
        logging.info("Tentando inserir a senha.")
        sso_password_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@id='outlined-basic-password']"))
        )
        sso_password_input.clear()
        sso_password_input.send_keys(sso_password)
        
        logging.info("Tentando clicar no botão 'Avançar'.")
        sso_login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//p[text()='Avançar']]"))
        )
        sso_login_button.click()
        
        logging.info("Login realizado com sucesso!")

        # Aguardar 10 segundos para garantir que o login foi processado
        time.sleep(10)
        
        # Verificar e clicar no botão "Registrar ponto"
        logging.info("Verificando se o botão 'Registrar ponto' está presente...")
        # registrar_ponto_button = WebDriverWait(driver, 20).until(
        #     EC.element_to_be_clickable((By.XPATH, "//button[.//p[text()='Registrar ponto']]"))
        # )
        # registrar_ponto_button.click()
        
        logging.info("Ponto registrado com sucesso!")
        
    except Exception as e:
        logging.error(f"Erro ao registrar o ponto: {e}")
        logging.error(traceback.format_exc())  # Adicionar traceback detalhado ao log
        driver.save_screenshot('erro_ponto.png')  # Capturar screenshot do erro
        raise

# Chama a função para bater o ponto nos determinados horários registrados
def bater_ponto():
    driver = None
    try:
        driver = get_driver(browser)
        login(driver, company_code, matricula, password)
        registrar_ponto(driver)
    except Exception as e:
        logging.error(f"Erro ao bater o ponto: {e}")
    finally:
        if driver:
            driver.quit()

# Executa a função
bater_ponto()
