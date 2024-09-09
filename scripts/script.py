from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # Importa o WebDriver Manager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Configurações do navegador (Chrome neste caso)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executar sem abrir o navegador
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Inicializa o navegador com o WebDriver Manager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Função para realizar o login e bater o ponto
def bater_ponto():
    try:
        # Acessa o site do Ahgora na página de nova batida
        driver.get("https://www.ahgora.com.br/novabatidaonline/")

        # Aguarda o site carregar
        time.sleep(5)

        # Clica no botão "Matrícula e senha"
        botao_matricula_senha = driver.find_element(By.XPATH, "//p[text()='Matrícula e senha']")
        botao_matricula_senha.click()

        # Aguarda o formulário aparecer
        time.sleep(2)

        # Preenche o código da empresa (primeiro campo)
        codigo_empresa_field = driver.find_elements(By.ID, "outlined-basic")[0]  # Primeiro campo de texto
        codigo_empresa_field.send_keys("305284")

        # Preenche a matrícula (segundo campo)
        matricula_field = driver.find_elements(By.ID, "outlined-basic")[1]  # Segundo campo de texto
        matricula_field.send_keys("a382748")

        # Preenche a senha
        senha_field = driver.find_element(By.ID, "outlined-password")
        senha_field.send_keys("@Agmtech100r")

        # Clica no botão "Liberar dispositivo"
        botao_liberar_dispositivo = driver.find_element(By.XPATH, "//p[text()='Liberar dispositivo']")
        botao_liberar_dispositivo.click()

        # Aguarda o login ser processado
        time.sleep(5)

        # Clica na opção "ACESSAR VIA SSO"
        botao_acessar_sso = driver.find_element(By.XPATH, "//p[text()='ACESSAR VIA SSO']")
        botao_acessar_sso.click()

        # Aguarda o redirecionamento para o SSO
        time.sleep(5)

        # Clica no botão "Registrar ponto"
        botao_registrar_ponto = driver.find_element(By.XPATH, "//p[text()='Registrar ponto']")
        botao_registrar_ponto.click()

        print("Ponto batido com sucesso!")
    except Exception as e:
        print(f"Erro ao bater o ponto: {e}")
    finally:
        driver.quit()

# Chama a função para bater o ponto
bater_ponto()
