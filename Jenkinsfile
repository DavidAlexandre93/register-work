pipeline {
    agent any

    environment {
        COMPANY_CODE = credentials('COMPANY_CODE') // Verifique se o ID das credenciais está correto
        MATRICULA = credentials('MATRICULA') // Verifique se o ID das credenciais está correto
        PASSWORD = credentials('PASSWORD') // Verifique se o ID das credenciais está correto
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
                    // Instalação de dependências específicas para ambiente Windows, se necessário
                    echo 'Preparando o ambiente para Windows...'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Verificar se Python e pip estão instalados
                    bat '''
                    python --version
                    pip install --upgrade pip
                    if not exist "%APPDATA%\\Python\\Scripts\\poetry.exe" (
                        pip install poetry
                    )
                    '''
                    // Instalar dependências com Poetry
                    bat 'poetry install'
                }
            }
        }

        stage('Setup ChromeDriver (Windows)') {
            steps {
                script {
                    // Certifique-se de que o Google Chrome e o ChromeDriver estejam instalados e no PATH
                    bat '''
                    SET CHROME_VERSION=Google Chrome --version | findstr /R /C:"[0-9]+\\.[0-9]+\\.[0-9]+"
                    SET CHROMEDRIVER_VERSION=curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_%CHROME_VERSION:~0,2%
                    curl -O https://chromedriver.storage.googleapis.com/%CHROMEDRIVER_VERSION%/chromedriver_win32.zip
                    tar -xf chromedriver_win32.zip
                    move /Y chromedriver.exe C:\\Windows\\System32\\chromedriver.exe
                    '''
                }
            }
        }

        stage('Run Selenium Script') {
            steps {
                script {
                    // Executa o script Python com as variáveis de ambiente necessárias
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
