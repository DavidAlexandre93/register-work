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

        stage('Install Poetry and Dependencies') {
            steps {
                script {
                    // Instalar o Poetry e as dependências do projeto
                    bat '''
                    if not exist "%APPDATA%\\Python\\Scripts\\poetry.exe" (
                        python -m pip install --upgrade poetry
                        if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                    )

                    if exist "pyproject.toml" (
                        poetry install --no-root
                        if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                    ) else (
                        echo "Arquivo pyproject.toml não encontrado!"
                        exit /b 1
                    )
                    '''
                }
            }
        }

        stage('Update All Dependencies') {
            steps {
                script {
                    // Atualizar todas as dependências para as versões mais recentes
                    bat '''
                    poetry update
                    if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                    '''
                }
            }
        }

        stage('Setup WebDriver (Windows)') {
            steps {
                script {
                    if (env.BROWSER == 'chrome') {
                        echo 'Configurando ChromeDriver...'
                        // Usar script Python para baixar o ChromeDriver mais atualizado
                        bat '''
                        poetry run python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
                        if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                        '''
                    } else if (env.BROWSER == 'firefox') {
                        echo 'Configurando GeckoDriver...'
                        // Usar script Python para baixar o GeckoDriver mais atualizado
                        bat '''
                        poetry run python -c "from webdriver_manager.firefox import GeckoDriverManager; GeckoDriverManager().install()"
                        if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
                        '''
                    } else if (env.BROWSER == 'edge') {
                        echo 'Configurando EdgeDriver...'
                        // Usar script Python para baixar o EdgeDriver mais atualizado
                        bat '''
                        poetry run python -c "from webdriver_manager.microsoft import EdgeChromiumDriverManager; EdgeChromiumDriverManager().install()"
                        if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%
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
