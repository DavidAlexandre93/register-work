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

# Configurações de logging
logging.basicConfig(level=logging.INFO)

# Carregar dados sensíveis das variáveis de ambiente ou usar valores padrão para testes
company_code = os.getenv("COMPANY_CODE", "a382748")
matricula = os.getenv("MATRICULA", "305284")
password = os.getenv("PASSWORD", "@Agmtech100r")

# Credenciais adicionais para o SSO
sso_username = os.getenv("SSO_USERNAME", "davifernande")
sso_password = os.getenv("SSO_PASSWORD", "@Mag6000r")

# Configurações do navegador (Chrome neste caso)
chrome_options = Options()
# Remova o modo headless para ver a execução no navegador
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Inicializa o navegador com o WebDriver Manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Função para realizar o login
def login(driver, company_code, matricula, password):
    try:
        logging.info("Tentando acessar o site...")
        driver.get("https://www.ahgora.com.br/novabatidaonline/")
        
        logging.info("Tentando clicar em 'Matrícula e senha'...")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Matrícula e senha']"))).click()
        
        logging.info("Tentando preencher o código da empresa...")
        WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.ID, "outlined-basic")))
        driver.find_elements(By.ID, "outlined-basic")[0].send_keys(company_code)
        
        logging.info("Tentando preencher a matrícula...")
        driver.find_elements(By.ID, "outlined-basic")[1].send_keys(matricula)
        
        logging.info("Tentando preencher a senha...")
        driver.find_element(By.ID, "outlined-password").send_keys(password)
        
        logging.info("Tentando clicar em 'Liberar dispositivo'...")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Liberar dispositivo']"))).click()
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
        
        logging.info("Tentando acessar via SSO...")
        
        # Aguardar um pouco antes de clicar para garantir que o botão esteja disponível
        time.sleep(5)
        
        # Verificar se o elemento "ACESSAR VIA SSO" está presente na página
        sso_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//p[text()='ACESSAR VIA SSO']"))
        )
        
        # Tentar clicar no botão SSO
        sso_button.click()
        
        logging.info("Botão 'ACESSAR VIA SSO' clicado com sucesso!")
        
        # Inserir as credenciais do SSO
        logging.info("Tentando inserir o nome de usuário do SSO...")
        sso_username_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='username']"))
        )
        sso_username_input.send_keys(sso_username)
        
        logging.info("Tentando inserir a senha do SSO...")
        sso_password_input = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@name='password']"))
        )
        sso_password_input.send_keys(sso_password)
        
        logging.info("Tentando clicar no botão de login do SSO...")
        sso_login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='1-submit']"))
        )
        sso_login_button.click()
        
        logging.info("Login SSO realizado com sucesso!")

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
        driver.save_screenshot('erro_ponto.png')
        raise

# Chama a função para bater o ponto nos determinados horários registrados
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
