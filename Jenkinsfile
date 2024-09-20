pipeline {
    agent any

    environment {
        COMPANY_CODE = credentials('COMPANY_CODE')
        MATRICULA = credentials('MATRICULA')
        PASSWORD = credentials('PASSWORD')
    }

    stages {
        stage('Verify Environment Variables') {
            steps {
                script {
                    echo 'Verificando as variáveis de ambiente...'
                    echo 'COMPANY_CODE: ****'
                    echo 'MATRICULA: ****'
                    echo 'PASSWORD: ****' // Nunca logar a senha
                }
            }
        }

        stage('Prepare Environment (Windows)') {
            steps {
                script {
                    echo 'Preparando o ambiente para Windows...'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Atualizar pip corretamente no Windows
                    bat '''
                    python -m pip install --upgrade pip
                    if not exist "C:\\WINDOWS\\system32\\config\\systemprofile\\AppData\\Roaming\\Python\\Scripts\\poetry.exe" (
                        pip install poetry
                    )
                    '''
                    
                    // Instalar dependências com Poetry, garantindo que o arquivo pyproject.toml esteja presente
                    bat '''
                    if exist "pyproject.toml" (
                        poetry install
                    ) else (
                        echo "Arquivo pyproject.toml não encontrado!"
                        exit /b 1
                    )
                    '''
                }
            }
        }

        stage('Setup ChromeDriver (Windows)') {
            steps {
                script {
                    // Usar alternativa para obter a versão do Chrome
                    bat '''
                    setlocal EnableDelayedExpansion
                    for /f "tokens=3" %%i in ('reg query "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon" /v version') do set CHROME_VERSION=%%i
                    if not defined CHROME_VERSION (
                        echo "Google Chrome não está instalado ou não foi possível obter a versão!"
                        exit /b 1
                    )
                    set CHROME_VERSION=!CHROME_VERSION:~0,-2!
                    set CHROMEDRIVER_VERSION=
                    for /f %%i in ('curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_!CHROME_VERSION!') do set CHROMEDRIVER_VERSION=%%i
                    if not defined CHROMEDRIVER_VERSION (
                        echo "Erro ao obter a versão do ChromeDriver!"
                        exit /b 1
                    )
                    curl -O https://chromedriver.storage.googleapis.com/!CHROMEDRIVER_VERSION!/chromedriver_win32.zip
                    tar.exe -xf chromedriver_win32.zip
                    move /Y chromedriver.exe C:\\Windows\\System32\\chromedriver.exe
                    endlocal
                    '''
                }
            }
        }

        stage('Run Selenium Script') {
            steps {
                script {
                    withEnv([
                        "COMPANY_CODE=${COMPANY_CODE}",
                        "MATRICULA=${MATRICULA}",
                        "PASSWORD=${PASSWORD}"
                    ]) {
                        bat 'poetry run python script.py'
                    }
                }
            }
        }
    }
}
