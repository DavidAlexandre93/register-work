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

        stage('Fix Pip Issues') {
            steps {
                script {
                    // Reinstalar o pip para corrigir possíveis problemas de distribuição inválida
                    bat '''
                    python -m pip uninstall pip setuptools -y
                    python -m ensurepip --upgrade
                    python -m pip install --upgrade pip setuptools
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Instala o Poetry e as dependências do projeto
                    bat '''
                    if not exist "C:\\WINDOWS\\system32\\config\\systemprofile\\AppData\\Roaming\\Python\\Scripts\\poetry.exe" (
                        pip install poetry
                    )
                    '''
                    
                    // Verifica se o arquivo pyproject.toml está presente e instala dependências
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
                    // Tentar obter a versão do Chrome de HKEY_CURRENT_USER e HKEY_LOCAL_MACHINE
                    bat '''
                    setlocal EnableDelayedExpansion
                    for /f "tokens=3" %%i in ('reg query "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon" /v version 2^>nul') do set CHROME_VERSION=%%i
                    if not defined CHROME_VERSION (
                        for /f "tokens=3" %%i in ('reg query "HKEY_LOCAL_MACHINE\\Software\\Google\\Chrome\\BLBeacon" /v version 2^>nul') do set CHROME_VERSION=%%i
                    )
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
