pipeline {
    agent any

    environment {
        // Use o ID correto das credenciais conforme configurado no Jenkins
        COMPANY_CODE = credentials('COMPANY_CODE_ID')
        MATRICULA = credentials('MATRICULA_ID')
        PASSWORD = credentials('PASSWORD_ID')
    }

    stages {
        stage('Verify Environment Variables') {
            steps {
                script {
                    echo "Verificando as variáveis de ambiente..."
                    echo "COMPANY_CODE: ${COMPANY_CODE}"
                    echo "MATRICULA: ${MATRICULA}"
                    echo "PASSWORD: ${PASSWORD}"
                }
            }
        }

        stage('Prepare Environment') {
            steps {
                script {
                    // Instala dependências necessárias para o Chrome e ChromeDriver
                    sh '''
                    sudo apt-get update
                    sudo apt-get install -y python3 python3-pip google-chrome-stable
                    sudo apt-get install -y wget unzip
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Instala o Poetry e as dependências do projeto
                    sh '''
                    pip install --upgrade pip
                    pip install poetry
                    poetry install
                    '''
                }
            }
        }

        stage('Setup ChromeDriver') {
            steps {
                script {
                    // Baixa e instala o ChromeDriver correspondente à versão do Google Chrome
                    sh '''
                    CHROME_VERSION=$(google-chrome --version | grep -oP '\\d+\\.\\d+\\.\\d+')
                    wget -N https://chromedriver.storage.googleapis.com/${CHROME_VERSION}/chromedriver_linux64.zip
                    unzip chromedriver_linux64.zip
                    sudo mv chromedriver /usr/bin/chromedriver
                    sudo chown root:root /usr/bin/chromedriver
                    sudo chmod +x /usr/bin/chromedriver
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
                        sh 'poetry run python script.py'
                    }
                }
            }
        }
    }

    post {
        always {
            // Limpa recursos após a execução
            echo 'Limpando recursos e arquivos temporários...'
            sh 'rm -f chromedriver_linux64.zip'
            cleanWs()
        }
        failure {
            echo 'Pipeline falhou. Verifique o log para detalhes.'
        }
    }
}
