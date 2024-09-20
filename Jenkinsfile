pipeline {
    agent any

    environment {
        COMPANY_CODE = credentials('COMPANY_CODE')
        MATRICULA = credentials('MATRICULA')
        PASSWORD = credentials('PASSWORD')
    }

    stages {

        stage('Verificar Feriados') {
            steps {
                script {
                    // Executa o script Python para verificar feriados
                    def resultado = bat(script: 'python verificar_feriados.py', returnStatus: true)
                    if (resultado != 0) {
                        error("Hoje é feriado! O job não será executado.")
                    }
                }
            }
        }

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
                    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

                    python -m ensurepip --upgrade
                    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

                    python -m pip install --upgrade pip setuptools
                    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Instalar o Poetry e as dependências do projeto
                    bat '''
                    if not exist "%APPDATA%\\Python\\Scripts\\poetry.exe" (
                        pip install poetry
                        if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                    )
                    '''
                    
                    // Verificar se o arquivo pyproject.toml está presente e instalar dependências
                    bat '''
                    if exist "pyproject.toml" (
                        poetry install
                        if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
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
                    // Tentar obter a versão do Chrome e baixar o ChromeDriver correspondente
                    bat '''
                    setlocal EnableDelayedExpansion
                    set CHROME_VERSION=
                    set CHROMEDRIVER_VERSION=
                    
                    for /f "tokens=3" %%i in ('reg query "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon" /v version 2^>nul') do set CHROME_VERSION=%%i
                    if not defined CHROME_VERSION (
                        for /f "tokens=3" %%i in ('reg query "HKEY_LOCAL_MACHINE\\Software\\Google\\Chrome\\BLBeacon" /v version 2^>nul') do set CHROME_VERSION=%%i
                    )
                    if not defined CHROME_VERSION (
                        echo "Google Chrome não está instalado ou versão não encontrada!"
                        echo "Usando versão padrão do ChromeDriver: 114.0.5735.90"
                        set CHROMEDRIVER_VERSION=114.0.5735.90
                    ) else (
                        set CHROME_VERSION=!CHROME_VERSION:~0,-2!
                        for /f %%i in ('curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_!CHROME_VERSION!') do set CHROMEDRIVER_VERSION=%%i
                    )

                    if not defined CHROMEDRIVER_VERSION (
                        echo "Erro ao obter a versão do ChromeDriver! Saindo."
                        exit /b 1
                    )
                    
                    echo "Usando versão do ChromeDriver: !CHROMEDRIVER_VERSION!"
                    curl -O https://chromedriver.storage.googleapis.com/!CHROMEDRIVER_VERSION!/chromedriver_win32.zip
                    tar.exe -xf chromedriver_win32.zip
                    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                    move /Y chromedriver.exe C:\\Windows\\System32\\chromedriver.exe
                    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                    del chromedriver_win32.zip
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
                        if (currentBuild.result == 'FAILURE') {
                            echo 'Falha na execução do script Selenium!'
                        }
                    }
                }
            }
        }
    }
}
