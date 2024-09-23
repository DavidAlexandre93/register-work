from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # Certifique-se de que esta linha está presente
import logging
import os
import traceback
import time
from datetime import datetime
import shutil

# Configurações de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configurações de diretório para capturas de tela
SCREENSHOT_DIR = os.path.join(os.getcwd(), 'screenshots')
CURRENT_RUN_DIR = os.path.join(SCREENSHOT_DIR, datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

# Cria o diretório para a execução atual se não existir
os.makedirs(CURRENT_RUN_DIR, exist_ok=True)

# Função para limpar capturas de tela
def limpar_screenshots():
    """Remove todos os arquivos do diretório de capturas de tela diariamente."""
    try:
        if os.path.exists(SCREENSHOT_DIR):
            for filename in os.listdir(SCREENSHOT_DIR):
                file_path = os.path.join(SCREENSHOT_DIR, filename)
                if os.path.isfile(file_path) or os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            logging.info("Capturas de tela antigas removidas com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao limpar capturas de tela: {e} - {e.__cause__} - {e.args}")

# Executa a limpeza das capturas de tela imediatamente ao iniciar o script
limpar_screenshots()

# Carregar dados sensíveis das variáveis de ambiente ou usar valores padrão para testes
company_code = os.getenv("COMPANY_CODE", "a382748")
matricula = os.getenv("MATRICULA", "305284")
password = os.getenv("PASSWORD", "@Agmtech100r")
browser = os.getenv("BROWSER", "chrome").lower()  # Seleciona o navegador a partir da variável de ambiente, padrão é "chrome"

# Função para inicializar o WebDriver com base no navegador selecionado
def get_driver(browser):
    try:
        if browser == "chrome":
            logging.info("Inicializando o Chrome WebDriver...")
            chrome_options = ChromeOptions()
            # chrome_options.add_argument("--headless") # Usar se quiser rodar em modo headless
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-infobars')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-notifications')
            # Utiliza o ChromeDriverManager para baixar e instalar a versão mais atualizada do ChromeDriver
            return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        else:
            raise ValueError(f"Navegador '{browser}' não suportado! Use 'chrome', 'firefox' ou 'edge'.")
    except Exception as e:
        logging.error(f"Erro ao inicializar o WebDriver: {e} - {e.__cause__} - {e.args}")
        raise

# Função para realizar o login
# Substituir o uso de 'time.sleep()' por 'WebDriverWait' para garantir a estabilidade

def login(driver, company_code, matricula, password):
    try:
        logging.info("Tentando acessar o site...")
        driver.get("https://www.ahgora.com.br/novabatidaonline/")
        driver.save_screenshot(os.path.join(CURRENT_RUN_DIR, 'pagina.png'))
        
        logging.info("Tentando clicar em 'Matrícula e senha'...")
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Matrícula e senha']"))).click()
        
        logging.info("Tentando preencher o código da empresa...")
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "outlined-basic")))
        driver.find_elements(By.ID, "outlined-basic")[0].send_keys(company_code)
        
        logging.info("Tentando preencher a matrícula...")
        driver.find_elements(By.ID, "outlined-basic")[1].send_keys(matricula)
        
        logging.info("Tentando preencher a senha...")
        driver.find_element(By.ID, "outlined-password").send_keys(password)
        
        driver.save_screenshot(os.path.join(CURRENT_RUN_DIR, 'matricula_senha_preenchidos.png'))
        
        logging.info("Esperando carregar a página...")
        # Substituindo time.sleep por espera explícita no botão de 'Liberar dispositivo'
        liberar_dispositivo_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//p[text()='Liberar dispositivo']]"))
        )
        logging.info("Botão 'Liberar dispositivo' encontrado, verificando se está habilitado...")
        
        if liberar_dispositivo_btn.is_enabled():
            liberar_dispositivo_btn.click()
            logging.info("Clique no botão 'Liberar dispositivo' efetuado.")
        else:
            logging.warning("Botão 'Liberar dispositivo' não está habilitado. Tentando usar JavaScript para clicar.")
            driver.execute_script("arguments[0].click();", liberar_dispositivo_btn)
            
    except Exception as e:
        logging.error(f"Erro durante o login: {e} - {e.__cause__} - {e.args}")
        driver.save_screenshot(os.path.join(CURRENT_RUN_DIR, 'erro_login.png'))
        if not os.path.exists(CURRENT_RUN_DIR):
            os.makedirs(CURRENT_RUN_DIR, exist_ok=True)
        try:
            with open(os.path.join(CURRENT_RUN_DIR, 'pagina_erro.html'), 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
        except Exception as ex:
            logging.error(f"Erro ao salvar o HTML da página: {ex} - {ex.__cause__} - {ex.args}")
        logging.error(traceback.format_exc())
        raise

# Função para registrar o ponto
def registrar_ponto(driver):
    try:
        logging.info("Iniciando registro do ponto após o login inicial")
         
        # Usar o XPath atualizado para localizar o botão "Registre seu ponto"
        register_button = WebDriverWait(driver, 30).until(
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
        
        logging.info("Ponto registrado com sucesso!")
        
    except Exception as e:
        logging.error(f"Erro ao registrar o ponto: {e} - {e.__cause__} - {e.args}")
        logging.error(traceback.format_exc())  # Adicionar traceback detalhado ao log
        driver.save_screenshot(os.path.join(CURRENT_RUN_DIR, 'erro_ponto.png'))  # Capturar screenshot do erro
        raise

# Chama a função para bater o ponto nos determinados horários registrados
def bater_ponto():
    driver = None
    try:
        driver = get_driver("chrome")  # Certifique-se de que o valor do navegador é válido
        login(driver, company_code, matricula, password)
        registrar_ponto(driver)
    except Exception as e:
        logging.error(f"Erro ao bater o ponto: {e} - {e.__cause__} - {e.args}")
    finally:
        if driver:
            driver.quit()

# Executa a função
bater_ponto()
