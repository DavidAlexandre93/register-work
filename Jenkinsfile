pipeline {
    agent any

    environment {
        COMPANY_CODE = credentials('COMPANY_CODE')
        MATRICULA = credentials('MATRICULA')
        PASSWORD = credentials('PASSWORD')
        BROWSER = 'chrome' // Pode ser alterado para 'firefox' ou 'edge'
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
                    echo "Navegador selecionado: ${BROWSER}"
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

        stage('Setup WebDriver (Windows)') {
            steps {
                script {
                    if (env.BROWSER == 'chrome') {
                        echo 'Configurando ChromeDriver...'
                        // Código de configuração do ChromeDriver aqui (igual ao original)
                        // ...
                    } else if (env.BROWSER == 'firefox') {
                        echo 'Configurando GeckoDriver...'
                        bat '''
                        set GECKODRIVER_VERSION=v0.31.0
                        curl -O https://github.com/mozilla/geckodriver/releases/download/%GECKODRIVER_VERSION%/geckodriver-%GECKODRIVER_VERSION%-win64.zip
                        if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                        tar.exe -xf geckodriver-%GECKODRIVER_VERSION%-win64.zip
                        if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                        move /Y geckodriver.exe C:\\Windows\\System32\\geckodriver.exe
                        if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                        del geckodriver-%GECKODRIVER_VERSION%-win64.zip
                        '''
                    } else if (env.BROWSER == 'edge') {
                        echo 'Configurando EdgeDriver...'
                        bat '''
                        set EDGEDRIVER_VERSION=114.0.1823.67
                        curl -O https://msedgedriver.azureedge.net/%EDGEDRIVER_VERSION%/edgedriver_win64.zip
                        if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                        tar.exe -xf edgedriver_win64.zip
                        if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                        move /Y msedgedriver.exe C:\\Windows\\System32\\msedgedriver.exe
                        if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                        del edgedriver_win64.zip
                        '''
                    } else {
                        error('Navegador não suportado! Use "chrome", "firefox" ou "edge".')
                    }
                }
            }
        }

        stage('Run Selenium Script') {
            steps {
                script {
                    withEnv([
                        "COMPANY_CODE=${COMPANY_CODE}",
                        "MATRICULA=${MATRICULA}",
                        "PASSWORD=${PASSWORD}",
                        "BROWSER=${BROWSER}"
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
