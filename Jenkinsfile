pipeline {
    agent any

    environment {
        // Use o ID correto das credenciais conforme configurado no Jenkins
        COMPANY_CODE = credentials('COMPANY_CODE_ID') // Verifique se o ID das credenciais está correto
        MATRICULA = credentials('MATRICULA_ID') // Verifique se o ID das credenciais está correto
        PASSWORD = credentials('PASSWORD_ID') // Verifique se o ID das credenciais está correto
    }

    stages {
        stage('Verify Environment Variables') {
            steps {
                script {
                    echo "Verificando as variáveis de ambiente..."
                    echo "COMPANY_CODE: ${COMPANY_CODE}"
                    echo "MATRICULA: ${MATRICULA}"
                    echo "PASSWORD: ${PASSWORD}" // Evite logar senhas em ambientes de produção
                }
            }
        }

        stage('Prepare Environment') {
            steps {
                script {
                    // Instala dependências necessárias para o Chrome e ChromeDriver, se não existirem
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
                    // Instala o Poetry e as dependências do projeto, se necessário
                    sh '''
                    pip install --upgrade pip
                    if ! command -v poetry &> /dev/null; then
                        pip install poetry
                    fi
                    poetry install
                    '''
                }
            }
        }

        stage('Setup ChromeDriver') {
            steps {
                script {
                    // Obtém a versão compatível do ChromeDriver e instala
                    sh '''
                    CHROME_VERSION=$(google-chrome --version | grep -oP '\\d+\\.\\d+\\.\\d+' | head -n1)
                    CHROMEDRIVER_VERSION=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION%.*})
                    wget -N https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip
                    unzip chromedriver_linux64.zip
                    sudo mv -f chromedriver /usr/bin/chromedriver
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
            script {
                echo 'Limpando recursos e arquivos temporários...'
                // Remoção de arquivos temporários e limpeza do workspace
                sh 'rm -f chromedriver_linux64.zip' // Isso pode ser simplificado já que cleanWs remove todos os arquivos
                cleanWs() // Limpa o workspace
            }
        }
        failure {
            echo 'Pipeline falhou. Verifique o log para detalhes.'
        }
    }
}
